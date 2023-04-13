import numpy as np
import cv2

def mosaico(img, order):
    # Divide in 4 horizontal strips (lines)
    lines = np.split(img, 4, axis=0)
    # Divide verticaly each line in 4 pieces (squares)
    squares = [np.split(line, 4, axis=1) for line in lines]
    # Placehold for the new order of squares
    new_squares = [[0 for _ in range(4)] for _ in range(4)]
    for k in range(16):
        i = order[k] - 1  # make the order start on index zero
        # Convert the order to the coordenate in the matrix
        new_squares[k // 4][k % 4] = squares[i // 4][i % 4]
    # Recombine to form the new horizontal lines
    new_lines = [np.concatenate(new_square, axis=1) for new_square in new_squares]
    # Recombine the horizontal lines into the new image
    new_img = np.concatenate(new_lines, axis=0)
    return new_img

def combinacao_imagem(img1, img2):
    return 0.5 * img1 + 0.5 * img2

def negativo(img):
    return np.invert(img)

def converter_para_intervalo(img):
    return 100 + (img / 255) * 100

def linhas_pares_invertidas(img):
    linhas_pares = img[::2]         # seleciona as linhas pares
    img[::2] = linhas_pares[:,::-1] # inverte as linhas
    return img

def reflexao_linhas(img):
    n, m = img.shape
    part1 = img[:m//2:]
    part2 = part1[::-1]
    return np.concatenate((part1, part2), axis=0)

def espelhamento_vertical(img):
    return img[::-1]

def colorida_colorida(img):
    # Set up the transformation matrix
    A = np.array([[0.393, 0.769, 0.189],
                  [0.349, 0.686, 0.168],
                  [0.272, 0.534, 0.131]])
    # Multiply each pixel by the transformation matrix
    img = np.dot(img, A)
    # Limit pixel values to the range [0, 255]
    return np.clip(img, 0, 255)

def colorida_cinza(img):
    # Set up the transformation matrix
    A = np.array([0.2989, 0.5870, 0.1140])
    # Multiply each pixel by the transformation matrix
    img = np.dot(img, A)
    # Limit pixel values to the range [0, 255]
    return np.clip(img, 0, 255)

def ajuste_brilho(img, gamma):
    img = (img / 255) ** (1 / gamma)
    factor = 255 / np.max(img)
    return img * factor

def quantizacao(img, l):
    img = (img / 255) * (l - 1)
    img = np.around(img)
    return img * (256/(l-1))

def planos_bit(img, plano):
    bit_planes = [np.uint8((img >> bit) & 1) for bit in range(8)]
    return bit_planes[plano] * 255

# Definição das matrizes
h1 = np.asarray([[0, 0, -1, 0, 0],
                 [0, -1, -2, -1, 0],
                 [-1, -2, 16, -2, -1],
                 [0, -1, -2, -1, 0],
                 [0, 0, -1, 0, 0]])
h2 = np.asarray([[1, 4, 6, 4, 1],
                 [4, 16, 24, 16, 4],
                 [6, 24, 36, 24, 6],
                 [4, 16, 24, 16, 4],
                 [1, 4, 6, 4, 1]])
h2 = h2 / 256
h3 = np.asarray([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
h4 = np.asarray([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
h5 = np.asarray([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
h6 = np.asarray([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9
h7 = np.asarray([[-1, -1, 2], [-1, 2, -1], [2, -1, -1]])
h8 = np.asarray([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]])
h9 = np.identity(9) / 9
h10 = np.asarray([[-1, -1, -1, -1, -1],
                  [-1, 2, 2, 2, -1],
                  [-1, 2, 8, 2, -1],
                  [-1, 2, 2, 2, -1],
                  [-1, -1, -1, -1, -1]])
h10 = h10 / 8
h11 = np.asarray([[1, -1, 0], [-1, 0, 1], [0, 1, 1]])

def filtragem(img, h):
    return cv2.filter2D(img, -1, h)

def filtragem_h3_h4(img):
    img = img.astype(np.float32)
    res = np.square(filtragem(img, h3))
    res += np.square(filtragem(img, h4))
    res = np.sqrt(res)
    return res
