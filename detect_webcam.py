import cv2
import numpy as np
import time
from datetime import datetime

# ========= CONFIGURAÇÕES AVANÇADAS =========
CONFIG = {
    # Cores dos carrinhos (valores HSV)
    "cores": {
        "carro_azul": {
            "lower": [100, 150, 50], 
            "upper": [140, 255, 255],
            "color": (255, 0, 0),  # Azul em BGR
            "destaque": (255, 255, 0)  # Amarelo para contorno
        },
        "carro_amarelo": {
            "lower": [20, 100, 100], 
            "upper": [40, 255, 255],
            "color": (0, 255, 255),  # Amarelo em BGR
            "destaque": (255, 0, 255)  # Rosa para contorno
        }
    },
    
    # Área de exclusão (ajuste conforme sua câmera)
    "zona_proibida": {
        "x1": 0, "y1": 0, 
        "x2": 300, "y2": 250,  # Tamanho da zona
        "color": (0, 0, 255)   # Vermelho
    },
    
    # Parâmetros de detecção
    "area_minima": 1200,       # Tamanho mínimo em pixels
    "proporcao": (1.3, 2.8),  # Largura/Altura esperada
    "cooldown": 3              # Segundos entre fotos
}

# ========= FUNÇÕES PROFISSIONAIS =========
def criar_interface(frame):
    """Cria uma interface visual impressionante"""
    # Header
    cv2.rectangle(frame, (0, 0), (640, 60), (40, 40, 40), -1)
    cv2.putText(frame, "DETECTOR DE CARRINHOS - IA PRO", (20, 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    
    # Footer
    cv2.rectangle(frame, (0, 420), (640, 480), (40, 40, 40), -1)
    cv2.putText(frame, "Pressione Q para sair", (20, 450), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Zona proibida
    cv2.rectangle(frame, 
                 (CONFIG["zona_proibida"]["x1"], CONFIG["zona_proibida"]["y1"]),
                 (CONFIG["zona_proibida"]["x2"], CONFIG["zona_proibida"]["y2"]),
                 CONFIG["zona_proibida"]["color"], 2)
    cv2.putText(frame, "AREA RESTRITA", 
               (CONFIG["zona_proibida"]["x1"]+10, CONFIG["zona_proibida"]["y1"]+20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, CONFIG["zona_proibida"]["color"], 1)

def melhorar_deteccao(mask):
    """Aprimora a máscara com técnicas profissionais"""
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Remove ruídos
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) # Preenche buracos
    return mask

def eh_carrinho_valido(x, y, w, h):
    """Filtros inteligentes combinados"""
    # 1. Fora da zona proibida
    if (x < CONFIG["zona_proibida"]["x2"] and y < CONFIG["zona_proibida"]["y2"]):
        return False
    
    # 2. Proporção realista para carrinhos
    proporcao = w / h
    if not (CONFIG["proporcao"][0] < proporcao < CONFIG["proporcao"][1]):
        return False
    
    # 3. Tamanho adequado
    area = w * h
    if area < CONFIG["area_minima"]:
        return False
    
    return True

# ========= PROGRAMA PRINCIPAL =========
def main():
    # Inicialização avançada
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("Erro: Câmera não encontrada!")
        return

    last_save = 0
    print("✅ SISTEMA INICIADO - APONTE OS CARRINHOS AZUL/AMARELO")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Prepara a visualização
        frame_visual = frame.copy()
        criar_interface(frame_visual)
        
        # Processamento em HSV (melhor para cores)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Detecta cada cor configurada
        for nome, valores in CONFIG["cores"].items():
            lower = np.array(valores["lower"], dtype=np.uint8)
            upper = np.array(valores["upper"], dtype=np.uint8)
            
            # Cria e aprimora a máscara
            mask = cv2.inRange(hsv, lower, upper)
            mask = melhorar_deteccao(mask)
            
            # Encontra contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                
                if eh_carrinho_valido(x, y, w, h):
                    # Desenha com efeito profissional
                    cv2.rectangle(frame_visual, (x, y), (x+w, y+h), valores["destaque"], 3)
                    cv2.rectangle(frame_visual, (x, y), (x+w, y+h), valores["color"], 2)
                    
                    # Texto com sombra
                    cv2.putText(frame_visual, nome.upper(), (x+2, y-12), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 3)
                    cv2.putText(frame_visual, nome.upper(), (x, y-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
                    
                    # Auto-save com timestamp
                    if time.time() - last_save > CONFIG["cooldown"]:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"detectado_{nome}_{timestamp}.jpg"
                        cv2.imwrite(filename, frame)
                        print(f"📸 {filename} salvo com sucesso!")
                        last_save = time.time()

        # Mostra o resultado
        cv2.imshow("Detector Profissional", frame_visual)
        
        # Sai com Q ou ESC
        if cv2.waitKey(1) in [ord('q'), 27]:
            break

    # Finalização
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Programa finalizado. Fotos salvas na pasta!")

if __name__ == "__main__":
    main()
