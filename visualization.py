import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def extract_depth(image_name):
    match = re.search(r'_(\d+\.?\d*)_x10', image_name)
    return float(match.group(1)) if match else None

def show_porosity_chart(df, window):
    chart_window = tk.Toplevel(window)
    chart_window.title("Gráfico de Porosidade")
    chart_window.geometry("800x600")

    df['Profundidade (m)'] = df['Imagem'].apply(extract_depth)
    df = df.dropna(subset=['Profundidade (m)']).sort_values(by='Profundidade (m)')

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(df['Profundidade (m)'], df['Porosidade (%)'], marker='o', linestyle='-', color='b', label="Porosidade (%)")
    ax.set_xlabel("Profundidade (m)")
    ax.set_ylabel("Porosidade (%)")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
