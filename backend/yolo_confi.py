import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from helpers.myutils import predict_yolo

# Caminho da imagem de teste
image_path = "/Xadrez/Xadrez_sistemas-Embarcados/datasets/images/all/0.png"  # Substitua pelo caminho de uma imagem real do tabuleiro

# Carregar a imagem
image = cv2.imread(image_path)
if image is None:
    print("Erro: Não foi possível carregar a imagem.")
    exit()

# Converter para RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Fazer a predição com YOLO
predictions_bboxes = predict_yolo(image_rgb)

# Exibir as detecções no console
print("\n🟢 Resultado das detecções com confiança:")
for bbox in predictions_bboxes:
    x1, y1, x2, y2, class_id, confidence = bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"], bbox["class"], bbox["confidence"]
    print(f"Peça detectada: {class_id} | Confiança: {confidence:.2f} | x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")

# Plotar a imagem com as detecções e a confiança
fig, ax = plt.subplots(1, figsize=(8, 8))
ax.imshow(image_rgb)

for bbox in predictions_bboxes:
    x1, y1, x2, y2, class_id, confidence = bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"], bbox["class"], bbox["confidence"]
    
    # Desenhar retângulo ao redor das peças detectadas
    rect = plt.Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, color="red", linewidth=2)
    ax.add_patch(rect)

    # Adicionar nome da peça detectada e a confiança
    ax.text(x1, y1 - 5, f"Peça {class_id} ({confidence:.2f})", color="red", fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

plt.show()
