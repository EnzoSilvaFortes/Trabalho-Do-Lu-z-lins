import cv2
import matplotlib.pyplot as plt

# Carrega o classificador Haarcascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Inicia a webcam
cap = cv2.VideoCapture(0)

# Captura apenas um frame
ret, frame = cap.read()
cap.release()

if not ret:
    print("Erro ao capturar imagem da webcam.")
    exit()

# Converte para cinza e detecta rosto
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

# Desenha os retângulos no frame original
for (x, y, w, h) in faces:
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Converte BGR -> RGB (pro matplotlib mostrar certo)
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Mostra com matplotlib
plt.imshow(frame_rgb)
plt.title("Detecção de Rosto")
plt.axis("off")
plt.show()
