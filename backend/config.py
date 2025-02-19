# backend/config.py

import torch

DEBUG = True
HOST = '127.0.0.1'
PORT = 8000
MODEL_PATH = "models/best.pt"  # Certifique-se de que o modelo está nesse caminho

# Caminho da pasta local do YOLOv5
YOLO_PATH = "/novo_projeto_xadrez/yolov5"

# Definir o dispositivo (GPU ou CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Carregar YOLOv5 localmente
model = torch.hub.load(YOLO_PATH, "custom", path=MODEL_PATH, source="local").to(device)
