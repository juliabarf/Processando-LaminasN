import csv
from openpyxl import load_workbook
import random
tamanhos = {
    'micropore': [],
    'mesopore': [],
    'megapore': [],
}

tamanhos['micropore'] = [round(random.uniform(0, 4), 2) for _ in range(8)]
tamanhos['mesopore'] = [round(random.uniform(4, 11), 2) for _ in range(8)]
tamanhos['megapore'] = [round(random.uniform(11, 14), 2) for _ in range(8)]


# Substitua 'nome_do_arquivo.xlsx' pelo caminho do seu arquivo
try:
    workbook = load_workbook(filename="planilhaModelo.xlsx")
    print("Arquivo aberto com sucesso!")

    # Acessar a primeira planilha
    sheet = workbook['dados']
    linha_C = linha_D = linha_E = linha_F = linha_G = linha_H = linha_I = linha_J = 4  # começa na linha 4 para Mesopore Very Small

    #coloca os valores na planilha
    for i, valor in enumerate(tamanhos['micropore']):
        sheet.cell(row=i + 4, column=2, value=valor)

    for valor in tamanhos['mesopore']:
        if valor < 0.25:
            sheet.cell(row=linha_C, column=3, value=valor)
            linha_C += 1
        elif valor < 0.5:
            sheet.cell(row=linha_D, column=4, value=valor)
            linha_D += 1
        elif valor < 1:
            sheet.cell(row=linha_E, column=5, value=valor)
            linha_E += 1
        elif valor < 2:
            sheet.cell(row=linha_F, column=6, value=valor)
            linha_F += 1
        elif valor < 4:
            sheet.cell(row=linha_G, column=7, value=valor)
            linha_G += 1

    for valor in tamanhos['megapore']:
        if valor < 12:
            sheet.cell(row=linha_H, column=8, value=valor)
            linha_H += 1
        elif valor < 13:
            sheet.cell(row=linha_I, column=9, value=valor)
            linha_I += 1
        elif valor < 14:
            sheet.cell(row=linha_J, column=10, value=valor)
            linha_J += 1


    # salva planilha nova
    workbook.save("planilhaModelo1.xlsx")


except FileNotFoundError:
    print("Erro: Arquivo não encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

print(tamanhos['micropore'])
print(tamanhos['mesopore'])
print(tamanhos['megapore'])


