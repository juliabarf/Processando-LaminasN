import customtkinter as ctk
from tkinter import messagebox
from file_operations import select_folder, save_to_excel, open_excel_file
from image_processing import crop_and_calculate_porosity
from visualization import show_porosity_chart
from gui_utils import run_in_thread, create_entry_with_label
from tkinter.ttk import Progressbar

def process_images():
    global df_porosity
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()

    if not input_folder or not output_folder:
        messagebox.showerror("Erro", "Por favor, selecione as pastas de entrada e saída.")
        return

    top, bottom = int(top_entry.get()), int(bottom_entry.get())
    left, right = int(left_entry.get()), int(right_entry.get())

    # Reseta a barra de progresso
    progress_bar["value"] = 0
    df_porosity = crop_and_calculate_porosity(input_folder, output_folder, top, bottom, left, right,progress_bar)
    save_to_excel(df_porosity, output_folder)
    messagebox.showinfo("Concluído", "Imagens processadas e resultados salvos!")

# Configuração da interface gráfica
window = ctk.CTk()
window.title("Processamento de Imagens")
window.geometry("1000x1000")

ctk.CTkLabel(window, text="Lagesed - Processamento de Lâminas", font=("Arial", 24, "bold")).pack(pady=10)

input_folder_entry = create_entry_with_label(window, "Pasta de Entrada")
ctk.CTkButton(window, text="Selecionar Pasta", command=lambda: select_folder(input_folder_entry)).pack(pady=3)

output_folder_entry = create_entry_with_label(window, "Pasta de Saída")
ctk.CTkButton(window, text="Selecionar Pasta", command=lambda: select_folder(output_folder_entry)).pack(pady=3)

top_entry = create_entry_with_label(window, "Topo")
bottom_entry = create_entry_with_label(window, "Fundo")
left_entry = create_entry_with_label(window, "Esquerda")
right_entry = create_entry_with_label(window, "Direita")

ctk.CTkButton(window, text="Processar Imagens", command=lambda: run_in_thread(process_images)).pack(pady=10)
progress_bar = Progressbar(window, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)
ctk.CTkButton(window, text="Visualizar Gráfico", command=lambda: show_porosity_chart(df_porosity, window)).pack(pady=5)
ctk.CTkButton(window, text="Abrir arquivo Excel", command=lambda: open_excel_file(output_folder_entry)).pack(pady=5)

window.mainloop()
