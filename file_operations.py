import os
import pandas as pd
from tkinter import filedialog, messagebox

def select_folder(entry_widget):
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_widget.delete(0, "end")
        entry_widget.insert(0, folder_path)

def save_to_excel(df, output_folder_path):
    excel_file_path = os.path.join(output_folder_path, 'porosidade_resultados.xlsx')
    df.to_excel(excel_file_path, index=False)
    messagebox.showinfo("Concluído", f"Tabela Excel salva em {excel_file_path}")

def open_excel_file(output_folder_entry):
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

