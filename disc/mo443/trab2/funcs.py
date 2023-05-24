import cv2 # pip install opencv-contrib-python
import numpy as np

def lin_global(img, threshold=128):
    # todos os pixels começam com preto
    res = np.zeros_like(img)
    # pixels com valor abaixo do limiar
    # são definidos como branco
    res[img < threshold] = 255
    return res

def otsu(img):
    _, img_thresholded = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img_thresholded

def local(img, f, window_size=25):
    # dimensões da imagem original
    height, width = img.shape
    # tamanho da janela
    w = window_size // 2
    # nova matriz para o resultado
    res = np.zeros_like(img)

    for i in range(height):
        for j in range(width):
            # limites da janela deslizante
            i_min = max(i - w, 0)
            i_max = min(i + w + 1, height)
            j_min = max(j - w, 0)
            j_max = min(j + w + 1, width)

            # A janela em questão
            window = img[i_min:i_max,
                         j_min:j_max]

            # Utiliza a função indicada
            # para calcular o limiar
            threshold = f(window)

            # em todos os casos, se o
            # valor do pixel é menor
            # que o limiar, ele é co-
            # lorido de branco
            if img[i,j] < threshold:
                res[i,j] = 255
    return res

def bernsen(window):
    # valor máximo e mínimo
    # dentro da janela
    max_val = int(np.max(window))
    min_val = int(np.min(window))

    return (max_val + min_val) // 2

def niblack(window, k=-0.2):
    # obter o valor médio e o desvio
    # padrão dentro da janela
    mean_val = int(np.mean(window))
    std_dev = int(np.std(window))

    # calcular o limiar usando a
    # fórmula de Niblack
    return mean_val + k * std_dev

def sauvola(window, k=0.5, R=128):
    mean_val = int(np.mean(window))
    std_dev = int(np.std(window))

    # fórmula de Sauvola e Pietaksinen
    aux = (1 + k * ((std_dev / R) - 1))
    return mean_val * aux

from math import exp
def phansalskar(window, p=2, q=10,
                k=0.25, R=0.5):
    mean_val = int(np.mean(window))
    std_dev = int(np.std(window))
    # componente a direita da fórmula
    aux = 1 + p * exp(-q * mean_val)
    aux += k * ( ( std_dev / R ) - 1 )
    # média vezes o componente a direita
    return mean_val * aux

def contraste(window):
    img_min = int(np.min(window))
    img_max = int(np.max(window))
    # média
    return (img_max + img_min) // 2

def media(window, cte=5):
    return int(np.mean(window)) - cte

def mediana(window):
    return np.median(window)
