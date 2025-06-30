import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
import numpy as np
import os
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import re


# Função para calcular a porosidade usando o método Otsu
def calculate_porosity(image):
    """
    Calcula a porosidade de uma imagem usando o método de segmentação Otsu.

    :param image: Imagem de entrada (matriz numpy).
    :return: Porosidade e imagem binarizada invertida.
    """
    ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    cb_channel = ycbcr[:, :, 2]
    _, BW_otsu = cv2.threshold(cb_channel, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    inverted_BW = cv2.bitwise_not(BW_otsu)
    total_area = BW_otsu.size
    white_area = np.sum(inverted_BW == 255)
    porosity = (white_area / total_area) * 100
    return porosity, inverted_BW

# Função para cortar as imagens e calcular a porosidade
def crop_and_calculate_porosity(input_folder_path, output_folder_path, top_border, bottom_border, left_border, right_border):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    results = []
    for file_name in os.listdir(input_folder_path):
        if file_name.endswith(('.jpg', '.jpeg', '.png', '.tiff')):
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

            # Calcular a porosidade da imagem cortada
            porosity, inverted_BW = calculate_porosity(cropped_image)
            output_file_name = os.path.splitext(new_file_name)[0] + '_otsu.png'
            output_image_path = os.path.join(output_folder_path, output_file_name)
            cv2.imwrite(output_image_path, inverted_BW)

            # Adicionar os resultados
            results.append({'Imagem': new_file_name, 'Porosidade (%)': porosity})

    df = pd.DataFrame(results)
    return df
# Função para abrir o arquivo Excel com os resultados
def open_excel_file():
    excel_file_path = os.path.join(output_folder_entry.get(), 'porosidade_resultados.xlsx')
    
    if not os.path.exists(excel_file_path):
        messagebox.showerror("Erro", "Arquivo 'porosidade_resultados.xlsx' não encontrado.")
        return

    # Tentar abrir o arquivo com o aplicativo padrão de planilhas
    try:
        if os.name == 'nt':  # Para Windows
            os.startfile(excel_file_path)
        elif os.name == 'posix':  # Para sistemas baseados em Unix (Linux/macOS)
            subprocess.call(['open', excel_file_path])  # macOS
            # subprocess.call(['xdg-open', excel_file_path])  # Para Linux, descomente se necessário
        else:
            messagebox.showerror("Erro", "Sistema operacional não suportado para abrir o arquivo automaticamente.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao tentar abrir o arquivo: {e}")


# Função para abrir o diálogo de seleção de pasta
def select_folder(entry_widget):
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_widget.delete(0, ctk.END)
        entry_widget.insert(0, folder_path)

# Função para exibir o DataFrame na interface gráfica



# Função para salvar o DataFrame em um arquivo Excel
def save_to_excel(df, output_folder_path):
    excel_file_path = os.path.join(output_folder_path, 'porosidade_resultados.xlsx')
    df.to_excel(excel_file_path, index=False)
    messagebox.showinfo("Concluído", f"Tabela Excel salva com sucesso em {excel_file_path}")

# Função para extrair profundidade do nome da imagem
def extract_depth(image_name):
    # Usar regex para capturar números com ou sem decimais antes de "_x10"
    match = re.search(r'_(\d+\.?\d*)_x10', image_name)
    if match:
        return float(match.group(1))  # Retorna a profundidade como número decimal
    else:
        return None  # Retorna None se não encontrar

# Função para abrir uma nova janela e mostrar o gráfico de porosidade
def show_porosity_chart(df):
    chart_window = ctk.CTkToplevel(window)
    chart_window.title("Gráfico de Porosidade")
    chart_window.geometry("800x600")

    # Adicionar coluna de profundidade ao DataFrame
    df['Profundidade (m)'] = df['Imagem'].apply(extract_depth)
    df = df.dropna(subset=['Profundidade (m)'])  # Remove linhas sem profundidade
    df = df.sort_values(by='Profundidade (m)')  # Ordena pelo eixo X (profundidade)

    # Criar gráfico
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(
        df['Profundidade (m)'], 
        df['Porosidade (%)'], 
        marker='o', 
        linestyle='-', 
        color='b', 
        label="Porosidade (%)"
    )
    ax.set_xlabel("Profundidade (m)")
    ax.set_ylabel("Porosidade (%)")
    ax.set_title("Tendência da Porosidade com a Profundidade")
    ax.legend()

    # Exibir gráfico na interface
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

# Função para processar as imagens ao clicar no botão
def process_images():
    global df_porosity  # Salvar o DataFrame globalmente para usá-lo no gráfico
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    if not input_folder or not output_folder:
        messagebox.showerror("Erro", "Por favor, selecione as pastas de entrada e saída.")
        return

    top_border = int(top_border_entry.get())
    bottom_border = int(bottom_border_entry.get())
    left_border = int(left_border_entry.get())
    right_border = int(right_border_entry.get())

    # Cortar as imagens e calcular a porosidade
    df_porosity = crop_and_calculate_porosity(input_folder, output_folder, top_border, bottom_border, left_border, right_border)

    # Exibir o DataFrame na interface gráfica
    #show_dataframe(df_porosity)

    # Salvar o DataFrame em Excel
    save_to_excel(df_porosity, output_folder)

    # Exibir uma mensagem de conclusão
    messagebox.showinfo("Concluído", "Imagens processadas e resultados salvos com sucesso!")

import threading
from tkinter import messagebox

# Função para processar imagens em um thread separado
def process_images_in_thread():
    # Usando threading para processar as imagens sem travar a interface
    processing_thread = threading.Thread(target=process_images)
    processing_thread.start()




# Criar a janela principal
window = ctk.CTk()
window.title("Processamento de Imagens")
window.geometry("1000x1000")
# Título da empresa
ctk.CTkLabel(window, text="Lagesed- Processamento de lâminas", font=("Arial", 24, "bold")).pack(pady=10)
ctk.CTkLabel(window, text="David Cubric Russo / Laboratório de Geologia Sedimentar UFRJ", font=("Arial", 16,)).pack(pady=10)

# Labels e caixas de entrada para pastas
ctk.CTkLabel(window, text="Pasta de Entrada").pack()
input_folder_entry = ctk.CTkEntry(window, width=150)
input_folder_entry.pack(pady=5)
ctk.CTkButton(window, text="Selecionar Pasta", height=30,command=lambda: select_folder(input_folder_entry)).pack(pady=5)

ctk.CTkLabel(window, text="Pasta de Saída").pack()
output_folder_entry = ctk.CTkEntry(window, width=150)
output_folder_entry.pack(pady=5 )
ctk.CTkButton(window, text="Selecionar Pasta", height=30,command=lambda: select_folder(output_folder_entry)).pack(pady=5)

# Labels e caixas de entrada para bordas de corte
ctk.CTkLabel(window, text="Bordas de Corte (px)").pack(pady=5)

ctk.CTkLabel(window, text="Topo").pack()
top_border_entry = ctk.CTkEntry(window)
top_border_entry.pack()

ctk.CTkLabel(window, text="Fundo").pack()
bottom_border_entry = ctk.CTkEntry(window)
bottom_border_entry.pack()

ctk.CTkLabel(window, text="Esquerda").pack()
left_border_entry = ctk.CTkEntry(window)
left_border_entry.pack()

ctk.CTkLabel(window, text="Direita").pack()
right_border_entry = ctk.CTkEntry(window)
right_border_entry.pack()

# Tabela para mostrar o DataFrame de porosidades
#tree = ttk.Treeview(window, columns=("Imagem", "Porosidade (%)"), show="headings", height=10)
#tree.heading("Imagem", text="Imagem")
#tree.heading("Porosidade (%)", text="Porosidade (%)")
#tree.pack(fill="x", pady=10)

# Botão para processar as imagens
# Agora, em vez de chamar process_images diretamente, você chama process_images_in_thread:
ctk.CTkButton(window, text="Processar Imagens", command=process_images_in_thread).pack(pady=10)

# Botão para visualizar o gráfico em uma nova janela
ctk.CTkButton(window, text="Visualizar Gráfico", command=lambda: show_porosity_chart(df_porosity)).pack(pady=5)
ctk.CTkButton(window, text="Abrir Planilha Excel", command=open_excel_file).pack(pady=5)

# Iniciar a interface gráfica
window.mainloop()
