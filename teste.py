import csv

tamanhos = {
    'micropore': [],
    'mesopore': [],
    'megapore': [],
}

for i in range(1, 6):
    tamanhos['micropore'].append(i)
    tamanhos['mesopore'].append(i+5)
    tamanhos['megapore'].append(i+5)


#print(tamanhos['micropore'][0])


# teste na planilha

from openpyxl import load_workbook

# Substitua 'nome_do_arquivo.xlsx' pelo caminho do seu arquivo
try:
    workbook = load_workbook(filename="planilhaModelo.xlsx")
    print("Arquivo aberto com sucesso!")

    # Acessar a primeira planilha
    sheet = workbook['dados']
    linha_C = linha_D = linha_E= linha_F= linha_G= linha_H= linha_I= linha_J = 4  # começa na linha 4 para Mesopore Very Small

    #adiciona valores micropore
    for i in range(len(tamanhos['micropore'])):
        valor_celula_a1 = sheet[f"B{i+4}"]
        if tamanhos['micropore'][i] < 6:
            valor_celula_a1.value = tamanhos['micropore'][i]

    for valor in tamanhos['mesopore']:
        if valor < 7:
            sheet[f"C{linha_C}"].value = valor
            linha_C += 1
        elif valor < 8:
            sheet[f"D{linha_D}"].value = valor
            linha_D += 1
        elif valor < 9:
            sheet[f"E{linha_E}"].value = valor
            linha_E += 1
        elif valor < 10:
            sheet[f"F{linha_F}"].value = valor
            linha_F += 1
        elif valor < 11:
            sheet[f"G{linha_G}"].value = valor
            linha_G += 1

    # Megapore
    for valor in tamanhos['megapore']:
        if valor not in tamanhos['megapore']:
            sheet[f"J{linha_H}"].value = ' '
            linha_H += 1
        if valor < 12:
            sheet[f"H{linha_H}"].value = valor
            linha_H += 1
        elif valor < 13:
            sheet[f"I{linha_I}"].value = valor
            linha_I += 1
        elif valor < 14:
            sheet[f"J{linha_J}"].value = valor
            linha_J += 1




    # salva planilha nova
    workbook.save("planilhaModelo1.xlsx")

except FileNotFoundError:
    print("Erro: Arquivo não encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

