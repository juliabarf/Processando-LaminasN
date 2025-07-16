import cv2
import numpy as np
import csv

# Configurações da imagem
image_path = "imagem35.jpg"  # Substitua com o caminho correto
image_width_mm = 26
image_height_mm = 18
image_width_px = 15191
image_height_px = 10692
pixel_area_mm2 = (image_width_mm * image_height_mm) / (image_width_px * image_height_px)

# Filtro de área mínima (em mm²)
area_minima_mm2 = 0.005

# Limiares para colorir os poros por tamanho
LIMIAR_PEQUENO = 0.02
LIMIAR_MEDIO = 0.1

# Carregar e processar imagem
img = cv2.imread(image_path)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Gerar imagem preto e branco (poros em branco)
bw_image = cv2.bitwise_and(img, img, mask=mask)
bw_gray = cv2.cvtColor(bw_image, cv2.COLOR_BGR2GRAY)
_, bw_binary = cv2.threshold(bw_gray, 1, 255, cv2.THRESH_BINARY)

# Encontrar contornos
contours, _ = cv2.findContours(bw_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Criar imagem de saída em BGR com fundo preto e poros brancos
output_base = np.zeros((bw_binary.shape[0], bw_binary.shape[1], 3), dtype=np.uint8)
output_base[bw_binary == 255] = (255, 255, 255)  # poros brancos

# Máscara para contagem real
mask_circles = np.zeros_like(bw_binary)
circle_areas_mm2 = []

# Processar poros detectados
for cnt in contours:
    area_px = cv2.contourArea(cnt)
    area_mm2 = area_px * pixel_area_mm2

    if area_mm2 >= area_minima_mm2:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)

        # Cor por tamanho
        if area_mm2 < LIMIAR_PEQUENO:
            color = (255, 0, 0)  # azul (pequeno)
        elif area_mm2 < LIMIAR_MEDIO:
            color = (0, 255, 255)  # amarelo (médio)
        else:
            color = (0, 0, 255)  # vermelho (grande)


        cv2.circle(output_base, center, radius, color, 4)  # espessura aumentada para 4

        # Preencher máscara de contagem
        cv2.circle(mask_circles, center, radius, 255, -1)

        # Salvar área
        circle_area_px = np.pi * (radius ** 2)
        circle_areas_mm2.append(circle_area_px * pixel_area_mm2)

# Calcular área real
pores_within_circles = cv2.bitwise_and(bw_binary, mask_circles)
white_pixels = cv2.countNonZero(pores_within_circles)
total_real_pore_area_mm2 = white_pixels * pixel_area_mm2

# Estatísticas
valid_pores = len(circle_areas_mm2)
mean_real_area = total_real_pore_area_mm2 / valid_pores if valid_pores > 0 else 0
mean_circle_area = np.mean(circle_areas_mm2) if valid_pores > 0 else 0

# --- SALVAR CSV ---
csv_path = "tamanhos_poros.csv"
with open(csv_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Poro", "Área do Círculo (mm²)"])
    for i, area in enumerate(circle_areas_mm2, 1):
        writer.writerow([i, area])
    writer.writerow([])
    writer.writerow(["Resumo"])
    writer.writerow(["Total de Poros (filtrados)", valid_pores])
    writer.writerow(["Área média real (pixels brancos)", mean_real_area])
    writer.writerow(["Área média dos círculos", mean_circle_area])
    writer.writerow(["Área mínima considerada (mm²)", area_minima_mm2])

# --- SALVAR IMAGEM ---
output_image_path = "poros_classificados.jpg"
cv2.imwrite(output_image_path, output_base)

print(f"CSV salvo como: {csv_path}")
print(f"Imagem com poros classificados salva como: {output_image_path}")
