import cv2
import numpy as np

def calcular_media_poros(image_path, mm_por_pixel):
    # Carrega a imagem
    image = cv2.imread(image_path)
    if image is None:
        print("Erro: imagem não encontrada.")
        return

    # Converte para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplica limiarização (inverso para que os poros fiquem brancos)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Encontra os contornos (poros)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calcula as áreas dos contornos em pixels
    areas_pixels = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) > 0]

    if len(areas_pixels) == 0:
        print("Nenhum poro detectado.")
        return

    # Converte as áreas para mm²
    areas_mm2 = [area * (mm_por_pixel ** 2) for area in areas_pixels]

    # Calcula a média
    media_area_mm2 = np.mean(areas_mm2)

    print(f"Número de poros detectados: {len(areas_mm2)}")
    print(f"Média da área dos poros: {media_area_mm2:.6f} mm²")

# Exemplo de uso:
#calcular dpi para achar o numero exato de pixels e mm
# Se 1 mm = 100 pixels => 1 pixel = 0.01 mm => mm_por_pixel = 0.01
calcular_media_poros("imagem2.png", mm_por_pixel=0.000332)
