import cv2
import numpy as np
from funcs import *

# Read all images in img folder
gray = ["baboon", "butterfly", "city", "house", "seagull"]

# Functions to gray images with one param to apply
funcs = [
    negativo,
    converter_para_intervalo,
    linhas_pares_invertidas,
    reflexao_linhas,
    espelhamento_vertical,
    filtragem_h3_h4,
]


def executar(func, file, param2=None):
    """
    Executa uma função e salva a imagem resultante.
    Pode ser utilizada para funções com 1 ou 2 parâmetros.

    Args:
        func (function): Função a ser executada
        file (str): Nome do arquivo a ser lido
        param2 (int, optional): Segundo parâmetro da função. Defaults to None.

    Returns:
        None
    """
    img = cv2.imread(f"img/{file}.png", cv2.IMREAD_GRAYSCALE)
    if param2 is not None:
        img = func(img, param2)
        cv2.imwrite(f"out/{file}_{func.__name__}_{str(param2)}.png", img)
    else:
        img = func(img)
        cv2.imwrite(f"out/{file}_{func.__name__}.png", img)


# Executar funções com 1 parâmetro
for f in funcs:
    for g in gray:
        executar(f, g)

# Combinação de imagens
for g in gray:
    for h in gray:
        if g != h:
            img1 = cv2.imread(f"img/{g}.png", cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(f"img/{h}.png", cv2.IMREAD_GRAYSCALE)
            img = combinacao_imagem(img1, img2)
            cv2.imwrite(f"out/{g}_{h}_combinacao.png", img)

# Brilho
gammas = [0.5, 1.5, 2.5, 3.5]
for g in gray:
    for gamma in gammas:
        executar(ajuste_brilho, g, gamma)

# Quantização
quant = [2, 4, 8, 16, 32, 64]
for g in gray:
    for q in quant:
        executar(quantizacao, g, q)

# Planos de bits
bits = range(8)
for g in gray:
    for b in bits:
        executar(planos_bit, g, b)

# Filtros
h = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11]
for g in gray:
    for f in range(len(h)):
        img = cv2.imread(f"img/{g}.png", cv2.IMREAD_GRAYSCALE)
        new_img = filtragem(img, h[f])
        cv2.imwrite(f"out/{g}_filtro_h{f+1}.png", new_img)


# Imagens coloridas
img = cv2.imread("img/lena.png", cv2.IMREAD_COLOR)
img = colorida_colorida(img)
cv2.imwrite("out/lena_colorida_colorida.png", img)

img = cv2.imread("img/lena.png", cv2.IMREAD_COLOR)
img = colorida_cinza(img)
cv2.imwrite("out/lena_colorida_cinza.png", img)

# Mosaico
img = cv2.imread("img/baboon.png", cv2.IMREAD_GRAYSCALE)
order = [6, 11, 13, 3, 8, 16, 1, 9, 12, 14, 2, 7, 4, 15, 10, 5]
img = mosaico(img, order)
cv2.imwrite("out/baboon_mosaico.png", img)
