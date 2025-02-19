# backend/helpers/myutils.py

import cv2
import numpy as np
from PIL import Image
from config import model  # Importando o modelo do config.py

def predict_yolo(image):
    """Detecta peças de xadrez em uma imagem."""
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(image_rgb)

    results = model(img_pil)
    bboxes = results.xyxy[0].cpu().numpy()

    predictions = []
    for bbox in bboxes:
        if len(bbox) < 6:
            continue  # Ignora casos inválidos

        x1, y1, x2, y2, conf, class_id = bbox[:6]

        if conf > 0.5:
            predictions.append({
                "class": int(class_id),
                "x1": int(x1), "y1": int(y1),
                "x2": int(x2), "y2": int(y2),
                "confidence": float(conf)
            })

    return predictions  # Retornando apenas previsões limpas
