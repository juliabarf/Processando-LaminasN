# script para automatizar as analises da pesquisa
"""
Classificação dos poros
referência de classificação:

-- > Coeficiente de variância

testes de imagens

--> imagem ideal e limpa
--> imagem com ruido
--> imagem escura/distorcida
--> imagem com diferentes resoluções
--> imagem sem poros
--> imagens com muitos poros
--> imagens inválidas ou corrompidas

"""
import numpy as np
from scipy import stats


def valor_medio(dados):
    soma = sum(dados)
    if not dados: return 0
    media = soma / len(dados)
    return media
def desvio_padrao(dados):
    if not dados: return 0
    return np.std(dados)
def erro_padrao(dados):
    dados = np.array(dados)
    dados = dados[~np.isnan(dados)]  # remove NaN, se houver

    if len(dados) < 2:
        return 0  # não dá pra calcular SEM

    return stats.sem(dados)
def incerteza(dados):
    dp = desvio_padrao(dados)
    if not dp: return 0
    return dp / (2 * (len(dados) - 1))
def predominante(dados):
    d0 = dados[0], [dados[1], dados[2], dados[3], dados[4],dados[5], dados[7], dados[8], dados[9]]
    classificacao0 = ['Micropore','Mesopore Very Small', 'Mesopore Small', 'Mesopore Medium', 'Mesopore Large', 'Mesopore Very Large', 'Megapore Small', 'Megapore Medium', 'Megapore Large']

    d1 = [dados[0], dados[6], dados[10]]
    classificacao1 = ['Micropore', 'Mesopore', 'Megapore']

    indice0 = classificacao0[max(range(len(d0)), key=lambda i: len(d0[i]))]
    indice1 = classificacao1[max(range(len(d1)), key=lambda i: len(d1[i]))]

    texto = f"{indice0} - {indice1}"

    return texto
