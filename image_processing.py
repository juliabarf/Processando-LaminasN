import cv2
import numpy as np
import os
import pandas as pd

def calculate_porosity(image):
    ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    cb_channel = ycbcr[:, :, 2]
    _, BW_otsu = cv2.threshold(cb_channel, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    inverted_BW = cv2.bitwise_not(BW_otsu)
    total_area = BW_otsu.size
    white_area = np.sum(inverted_BW == 255)
    porosity = (white_area / total_area) * 100
    return porosity, inverted_BW

def calculate_area_porosity(image):
    # Cada pixel representa 0.5 µm²
    area_por_pixel_um2 = 0.5

    # Converte a imagem para o espaço de cor YCrCb
    ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

    # Extrai o canal Cb (índice 2)
    cb_channel = ycbcr[:, :, 2]

    # Aplica limiarização de Otsu no canal Cb
    _, BW_otsu = cv2.threshold(cb_channel, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Inverte a imagem binária
    inverted_BW = cv2.bitwise_not(BW_otsu)

    # Calcula a área total e a área branca (poros)
    total_area = BW_otsu.size
    white_area = np.sum(inverted_BW == 255)

    # Calcula a porosidade da área em mm² (com conversão de µm² para mm²)
    area_porosity = (white_area * area_por_pixel_um2) / 1e6

    return area_porosity, inverted_BW


def crop_and_calculate_porosity(input_folder_path, output_folder_path, top_border, bottom_border, left_border, right_border, progress_bar):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    file_list = [f for f in os.listdir(input_folder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.tiff'))]
    total_files = len(file_list)
    results = []

    for idx, file_name in enumerate(file_list):
        image_path = os.path.join(input_folder_path, file_name)
        img = cv2.imread(image_path)

        if img is None:
            print(f"Não foi possível carregar a imagem {file_name}")
            continue

        height, width, _ = img.shape
        start_y = top_border
        end_y = height - bottom_border
        start_x = left_border
        end_x = width - right_border

        if start_y >= end_y or start_x >= end_x:
            print(f"As dimensões de corte excedem o tamanho da imagem {file_name}")
            continue

        # Cortar a imagem
        cropped_image = img[start_y:end_y, start_x:end_x]
        new_file_name = f"{os.path.splitext(file_name)[0]}_cropped{os.path.splitext(file_name)[1]}"
        new_image_path = os.path.join(output_folder_path, new_file_name)
        cv2.imwrite(new_image_path, cropped_image)

        # Calcular a porosidade
        porosity, inverted_BW = calculate_porosity(cropped_image)
        output_file_name = os.path.splitext(new_file_name)[0] + '_otsu.png'
        output_image_path = os.path.join(output_folder_path, output_file_name)
        cv2.imwrite(output_image_path, inverted_BW)

        # Calcular a área da porosidade
        porosity_area, inverted_BWs = calculate_area_porosity(cropped_image)
        output_file_name = os.path.splitext(new_file_name)[0] + '_otsu.png'
        output_image_path = os.path.join(output_folder_path, output_file_name)
        cv2.imwrite(output_image_path, inverted_BWs)

        results.append({'Imagem': new_file_name, 'Porosidade (%)': porosity, 'Área Porosidade (mm²)': porosity_area})

        # Atualizar a barra de progresso
        progress_bar["value"] = (idx + 1) / total_files * 100
        progress_bar.update_idletasks()

    df = pd.DataFrame(results)
    return df