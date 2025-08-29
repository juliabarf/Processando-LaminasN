import csv
import openpyxl
from numpy.ma.extras import column_stack
from openpyxl import load_workbook
import random
import pandas as pd
from analiseEstatistica import valor_medio, desvio_padrao, erro_padrao, incerteza, predominante
import win32com.client as win32

def testeMedia():
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





def testeEst():
    # Carregar a planilha
    workbook = load_workbook("planilhaModelo1.xlsx")
    sheet = workbook['dados'] # ou workbook["NomeDaAba"]

    # Pegar todas as linhas a partir da linha 4
    micropore = {
        'micropore': []
    }
    mesopore = {
        'mesoporeVerySmall': [],
        'mesoporeSmall': [],
        'mesoporeMedium': [],
        'mesoporeLarge': [],
        'mesoporeVeryLarge': []
    }
    megapore = {
        'megaporeSmall': [],
        'megaporeMedium': [],
        'megaporeLarge': []
    }


    #dados do micropore
    for row in sheet.iter_rows(min_row=4, min_col=2, max_col=2, values_only=True):
        micropore['micropore'].append(list(row))
    micropore = [row[0] for row in micropore['micropore'] if row[0] is not None]


    #DADOS MESOPORE
    for row in sheet.iter_rows(min_row=4, min_col=3, max_col=3, values_only=True):
        mesopore['mesoporeVerySmall'].append(list(row))
    mesoporeVerySmall = [row[0] for row in mesopore['mesoporeVerySmall'] if row[0] is not None]


    for row in sheet.iter_rows(min_row=4, min_col=4, max_col=4, values_only=True):
        mesopore['mesoporeSmall'].append(list(row))
    mesoporeSmall = [row[0] for row in mesopore['mesoporeSmall'] if row[0] is not None]

    for row in sheet.iter_rows(min_row=4, min_col=5, max_col=5, values_only=True):
        mesopore['mesoporeMedium'].append(list(row))
    mesoporeMedium = [row[0] for row in mesopore['mesoporeMedium'] if row[0] is not None]

    for row in sheet.iter_rows(min_row=4, min_col=6, max_col=6, values_only=True):
        mesopore['mesoporeLarge'].append(list(row))
    mesoporeLarge = [row[0] for row in mesopore['mesoporeLarge'] if row[0] is not None]

    for row in sheet.iter_rows(min_row=4, min_col=7, max_col=7, values_only=True):
        mesopore['mesoporeVeryLarge'].append(list(row))
    mesoporeVeryLarge = [row[0] for row in mesopore['mesoporeVeryLarge'] if row[0] is not None]

    mesopore_all = [valor[0] for lista in mesopore.values() for valor in lista if valor[0] is not None]


    #DADOS MEGAPORE
    for row in sheet.iter_rows(min_row=4, min_col=8, max_col=8, values_only=True):
        megapore['megaporeSmall'].append(list(row))
    megaporeSmall = [row[0] for row in megapore['megaporeSmall'] if row[0] is not None]

    for row in sheet.iter_rows(min_row=4, min_col=9, max_col=9, values_only=True):
        megapore['megaporeMedium'].append(list(row))
    megaporeMedium = [row[0] for row in megapore['megaporeMedium'] if row[0] is not None]

    for row in sheet.iter_rows(min_row=4, min_col=10, max_col=10, values_only=True):
        megapore['megaporeLarge'].append(list(row))
    megaporeLarge = [row[0] for row in megapore['megaporeLarge'] if row[0] is not None]

    megapore_all = [valor[0] for lista in megapore.values() for valor in lista if valor[0] is not None]




    print(micropore)
    print(mesoporeVerySmall)
    print(mesoporeSmall)
    print(mesoporeMedium)
    print(mesoporeLarge)
    print(mesoporeVeryLarge)
    print(megaporeSmall)
    print(megaporeMedium)
    print(megaporeLarge)
    soma = len(megaporeMedium)
    print(megapore_all)
    print(mesopore_all)
    print(valor_medio(megaporeMedium))
    valores = micropore, mesoporeVerySmall, mesoporeSmall, mesoporeMedium, mesoporeLarge, mesoporeVeryLarge, mesopore_all, megaporeSmall, megaporeMedium, megaporeLarge, megapore_all
    testeatualizaExcel(valores)

def testeatualizaExcel(valores):
    wb = load_workbook("planilhaModelo1.xlsx")
    aba = wb['analise']  # ou wb["NomeDaAba"]


    #atualiza com valor médio
    for j, valor in enumerate(valores, start=1):
        if valor:  # se não for lista vazia
            media = valor_medio(valor)
        else:
            media = "N/A"   # pode ser 0, None ou "N/A", depende do que você quer na planilha
        aba.cell(row=4, column=j+1, value=media)

    for j, valor in enumerate(valores, start=1):
        if valor:  # se não for lista vazia
            dp = desvio_padrao(valor)
        else:
            dp = "N/A"   # pode ser 0, None ou "N/A", depende do que você quer na planilha
        aba.cell(row=5, column=j+1, value=dp)

    for j, valor in enumerate(valores, start=1):
        if valor:  # se não for lista vazia
            ep = erro_padrao(valor)
        else:
            ep = "N/A"   # pode ser 0, None ou "N/A", depende do que você quer na planilha
        aba.cell(row=6, column=j+1, value=ep)

    for j, valor in enumerate(valores, start=1):
        if valor:  # se não for lista vazia
            inc = incerteza(valor)
        else:
            inc = "N/A"   # pode ser 0, None ou "N/A", depende do que você quer na planilha
        aba.cell(row=7, column=j+1, value=inc)

    wb.save("planilhaModelo1.xlsx")  # ou outro nome para não sobrescrever

def teste_histograma():


    # Abrir Excel
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    excel.Visible = True  # mostra o Excel

    # Abrir planilha existente
    wb = excel.Workbooks.Open(r'C:\Users\JuliaBarbosa\Downloads\Processando-LaminasN\planilhaModelo1.xlsx')
    ws = wb.Sheets('dados')

    # Selecionar intervalo de dados
    dados_range = ws.Range('B4:B11')  # ajuste conforme seus dados

    # Criar histograma
    chart = ws.Shapes.AddChart2(201, 51, 300, 10, 500, 300)  # 201=histograma, 51=coluna
    chart.Chart.SetSourceData(dados_range)

    # Salvar e fechar
    wb.Save()
    wb.Close()
    excel.Quit()































