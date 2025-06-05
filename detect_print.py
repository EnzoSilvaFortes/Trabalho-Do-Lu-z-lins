import cv2
from ultralytics import YOLO
import time

# Carregue seu modelo treinado (ajuste o caminho se necessário)
model = YOLO('runs/detect/train/weights/best.pt')

# Abre a webcam (0 é a webcam padrão)
cap = cv2.VideoCapture(0)

saved = False  # flag para evitar salvar várias prints iguais

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detecta no frame atual
    results = model(frame)

    # Variável para marcar se detectou carrinho nesse frame
    detected = False

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()

        for box, score in zip(boxes, scores):
            if score > 0.3:  # confiança mínima, pode ajustar
                detected = True
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'Carrinho {score:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Se detectou e ainda não salvou print, salva
    if detected and not saved:
        timestamp = int(time.time())
        cv2.imwrite(f'print_carrinho_{timestamp}.jpg', frame)
        print(f'[INFO] Print salvo como print_carrinho_{timestamp}.jpg')
        saved = True  # evita salvar prints toda hora

    # Mostra o vídeo com as detecções
    cv2.imshow('Detecção de Carrinho - Pressione Q para sair', frame)

    # Aperte 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
