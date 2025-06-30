import tkinter as tk
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

# Função para abrir o diálogo de seleção de pasta
def select_folder(entry_widget):
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder_path)

# Função para exibir o DataFrame na interface gráfica
def show_dataframe(df):
    # Limpar qualquer tabela anterior
    for i in tree.get_children():
        tree.delete(i)
    
    # Inserir os dados no Treeview
    for index, row in df.iterrows():
        tree.insert("", "end", values=(row['Imagem'], f"{row['Porosidade (%)']:.2f}"))

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


# Função para plotar o gráfico de linha de porosidade
# Modifique a função de gráfico para evitar sobreposição
# Função para abrir uma nova janela e mostrar o gráfico de porosidade
def show_porosity_chart(df):
    chart_window = tk.Toplevel(window)
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
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
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
    show_dataframe(df_porosity)

    # Salvar o DataFrame em Excel
    save_to_excel(df_porosity, output_folder)

    # Plotar o gráfico de porosidade
    #plot_porosity_chart(df_porosity)

    # Exibir uma mensagem de conclusão
    messagebox.showinfo("Concluído", "Imagens processadas e resultados salvos com sucesso!")


# Criar a janela principal
window = tk.Tk()
window.title("Processamento de Imagens")
window.geometry("1000x1000")
# Título da empresa
tk.Label(window, text="Lagesed- Processamento de lâminas", font=("Arial", 24, "bold"), fg="black").pack(pady=10)
tk.Label(window, text="Autor: David Cubric Russo", font=("Arial", 16,), fg="black").pack(pady=10)
# Labels e caixas de entrada para pastas
tk.Label(window, text="Pasta de Entrada").pack()
input_folder_entry = tk.Entry(window, width=50)
input_folder_entry.pack()
tk.Button(window, text="Selecionar Pasta", command=lambda: select_folder(input_folder_entry)).pack()

tk.Label(window, text="Pasta de Saída").pack()
output_folder_entry = tk.Entry(window, width=50)
output_folder_entry.pack()
tk.Button(window, text="Selecionar Pasta", command=lambda: select_folder(output_folder_entry)).pack()

# Labels e caixas de entrada para bordas de corte
tk.Label(window, text="Bordas de Corte (px)").pack()

tk.Label(window, text="Topo").pack()
top_border_entry = tk.Entry(window)
top_border_entry.pack()

tk.Label(window, text="Fundo").pack()
bottom_border_entry = tk.Entry(window)
bottom_border_entry.pack()

tk.Label(window, text="Esquerda").pack()
left_border_entry = tk.Entry(window)
left_border_entry.pack()

tk.Label(window, text="Direita").pack()
right_border_entry = tk.Entry(window)
right_border_entry.pack()

# Tabela para mostrar o DataFrame de porosidades
tree = ttk.Treeview(window, columns=("Imagem", "Porosidade (%)"), show="headings", height=10)
tree.heading("Imagem", text="Imagem")
tree.heading("Porosidade (%)", text="Porosidade (%)")
tree.pack(fill="x", pady=10)
# Botão para visualizar o gráfico em uma nova janela
tk.Button(window, text="Visualizar Gráfico", command=lambda: show_porosity_chart(df_porosity)).pack()
# Botão para processar as imagens
tk.Button(window, text="Processar Imagens", command=process_images).pack()

# Iniciar a interface gráfica
window.mainloop()
