import cv2
import numpy as np
import csv


def calculate_media(image):
    #calcular os pixels em mm -- mm/pix
    image_path = image  # Substitua com o caminho correto
    image_width_mm = 26
    image_height_mm = 18
    image_width_px = 15191
    image_height_px = 10692
    pixel_area_mm2 = (image_width_mm * image_height_mm) / (image_width_px * image_height_px)

    #filtro em área minima
    area_minima_mm2 = 0.005

    #classificação dos tamanhos
    LIMIAR_PEQUENO = 0.02
    LIMIAR_MEDIO = 0.1

    #carrega e processa imagem
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    #gera imagem preto e branco - os poros estão em branco
    bw_image = cv2.bitwise_and(img, img, mask=mask)
    bw_gray = cv2.cvtColor(bw_image, cv2.COLOR_BGR2GRAY)
    _, bw_binary = cv2.threshold(bw_gray, 1, 255, cv2.THRESH_BINARY)

    #encontra contornos
    contours, _ = cv2.findContours(bw_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Criar imagem de saída em BGR com fundo preto e poros brancos
    output_base = np.zeros((bw_binary.shape[0], bw_binary.shape[1], 3), dtype=np.uint8)
    output_base[bw_binary == 255] = (255, 255, 255)  # poros brancos

    # Máscara para contagem real
    mask_circles = np.zeros_like(bw_binary)
    circle_areas_mm2 = []
    area_azul = []
    area_amarelo = []
    area_vermelho = []

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
                color = (255, 0, 0)  #azul
                area_azul.append(area_mm2)
            elif area_mm2 < LIMIAR_MEDIO:
                color = (0, 255, 255)  #amarelo
                area_amarelo.append(area_mm2)
            else:
                color = (0, 0, 255)  #vermelho
                area_vermelho.append(area_mm2)

            cv2.circle(output_base, center, radius, color, 15)  # espessura aumentada para 4

            # Preencher máscara de contagem
            cv2.circle(mask_circles, center, radius, 255, -1)

            # Salvar área
            circle_area_px = np.pi * (radius ** 2)
            circle_areas_mm2.append(circle_area_px * pixel_area_mm2)

    # Calcular área real
    pores_within_circles = cv2.bitwise_and(bw_binary, mask_circles)
    white_pixels = cv2.countNonZero(pores_within_circles)
    total_real_pore_area_mm2 = white_pixels * pixel_area_mm2

    #validação dos poros: precisa ser maior que 0 para ser valido para o calculo
    valid_pores = len(circle_areas_mm2)
    mean_real_area = total_real_pore_area_mm2 / valid_pores if valid_pores > 0 else 0
    mean_circle_area = np.mean(circle_areas_mm2) if valid_pores > 0 else 0

    # --- SALVAR CSV ---
    csv_path = "tamanhos_poros.csv"
    with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Poro', 'Poro pequeno', 'Poro médio', 'Poro grande'])

        # Encontra o maior tamanho entre as listas para evitar IndexError
        max_len = max(len(area_azul), len(area_amarelo), len(area_vermelho))

        # Preenche as linhas com os valores, usando "" quando não houver valor na posição
        for i in range(max_len):
            azul = area_azul[i] if i < len(area_azul) else ""
            amarelo = area_amarelo[i] if i < len(area_amarelo) else ""
            vermelho = area_vermelho[i] if i < len(area_vermelho) else ""
            writer.writerow([i + 1, azul, amarelo, vermelho])
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
    print(area_azul)
    print(area_amarelo)
    print(area_vermelho)

