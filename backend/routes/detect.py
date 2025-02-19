from flask import Blueprint, request, send_file
import cv2
import numpy as np
import io
import chess
import chess.svg
import cairosvg
from PIL import Image
from helpers.myutils import predict_yolo
from config import model

detect_bp = Blueprint("detect", __name__)

# Criar um tabuleiro de xadrez virtual
board = chess.Board()
x_chess_board = 'abcdefgh'

def generate_chessboard_image():
    """Gera a imagem do tabuleiro virtual atualizado."""
    svg_data = chess.svg.board(board, size=480)
    png_data = cairosvg.svg2png(bytestring=svg_data)
    return Image.open(io.BytesIO(png_data)).convert("RGB")

@detect_bp.route("/upload", methods=["POST"])
def upload_image():
    """Recebe uma imagem, detecta peças e retorna um tabuleiro virtual atualizado."""
    if "image" not in request.files:
        return {"error": "Nenhuma imagem enviada"}, 400

    file = request.files["image"]
    image_bytes = file.read()

    # Processar a imagem recebida
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_np = np.asarray(image, dtype=np.uint8)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Obter dimensões da imagem original
    altura_original, largura_original, _ = image_np.shape

    # Fazer predições com YOLO
    predictions_bboxes = predict_yolo(image_np)

    # Atualizar o tabuleiro virtual com as peças detectadas
    board.clear()  # Limpa o tabuleiro antes de atualizar

    # Definir tamanho do tabuleiro 8x8
    casas_x = largura_original / 8
    casas_y = altura_original / 8

    # Criar um conjunto para evitar sobreposição
    ocupados = set()

    # **1️⃣ Mapear os índices do YOLO para notação FEN**
    piece_map = {
        0: "P",  1: "p",  2: "R",  3: "r",
        4: "N",  5: "n",  6: "B",  7: "b",
        8: "K",  9: "k", 10: "Q", 11: "q"
    }

    for peca in predictions_bboxes:
        x1, y1, x2, y2, class_id, confidence = (
            peca["x1"], peca["y1"], peca["x2"], peca["y2"], peca["class"], peca["confidence"]
        )

        # Filtrar por confiança mínima
        if confidence < 0.65:
            print(f"⚠️ Ignorando classe {class_id} com baixa confiança ({confidence:.2f})")
            continue

        # **2️⃣ Verificar se a classe está no dicionário**
        piece_fen = piece_map.get(class_id, "")

        if piece_fen == "":
            print(f"⚠️ Classe {class_id} não encontrada no mapeamento, ignorando...")
            continue

        # **3️⃣ Calcular a posição no tabuleiro**
        col = min(7, max(0, int(((x1 + x2) / 2) // casas_x)))
        row = min(7, max(0, 7 - int(((y1 + y2) / 2) // casas_y)))  # Inverte a ordem das linhas

        # Evitar sobreposição
        if (col, row) in ocupados:
            print(f"⚠️ Posição {col},{row} já ocupada, ignorando peça {piece_fen}.")
            continue

        board.set_piece_at(chess.square(col, row), chess.Piece.from_symbol(piece_fen))
        ocupados.add((col, row))  # Marcar como ocupada
        print(f"✅ Peça detectada: {piece_fen} ({class_id}) em ({col}, {row}) com {confidence:.2f}")

    # Criar a nova imagem do tabuleiro atualizado
    updated_board_image = generate_chessboard_image()

    # Enviar a imagem gerada para o frontend
    output_buffer = io.BytesIO()
    updated_board_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return send_file(output_buffer, mimetype="image/png")
