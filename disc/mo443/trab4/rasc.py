import numpy as np
import cv2
from math import ceil
from arg_parser import args


def scale_and_rotate_image(
    image, scale_factor, angle, output_dimension, interpolation_method
):
    # Obter a altura e largura da imagem
    height, width = image.shape[:2]

    # Calcular o centro da imagem
    center = (width // 2, height // 2)

    # converter angle para radianos
    angle = np.deg2rad(angle)

    # Criar uma imagem com a dimensão output_dimension em preto
    scaled_rotated_image = np.zeros(
        (output_dimension[1], output_dimension[0], 3), np.uint8
    )

    # A matriz map indica de onde o pixel (x,y) da imagem de saída deve ser
    # obtido na imagem de entrada.
    map = np.zeros((output_dimension[0], output_dimension[1], 2), np.float32)
    center_out = (output_dimension[0] // 2, output_dimension[1] // 2)
    for x in range(output_dimension[0]):
        for y in range(output_dimension[1]):
            # aplicar a escala baseado na distância do pixel ao centro da imagem
            map[y, x] = (
                (y - center_out[0]) * 1 / scale_factor,
                (x - center_out[1]) * 1 / scale_factor,
            )
            # aplicar a rotação utilizando a formula da inversa da rotação
            # x' = cos(a)x + sin(a)y e
            # y' = - sin(a)x + cos(a)y
            map[y, x] = (
                map[y, x][0] * np.cos(angle) + map[y, x][1] * np.sin(angle),
                map[y, x][1] * np.cos(angle) - map[y, x][0] * np.sin(angle),
            )
            # transladar de volta ao centro
            map[y, x] = (
                map[y, x][0] + center_out[0],
                map[y, x][1] + center_out[1],
            )

    for x in range(output_dimension[0]):
        for y in range(output_dimension[1]):
            scaled_rotated_image[y, x] = interpolation_method(image, *map[y, x])

    return scaled_rotated_image


def proximo(img, x, y):
    return img[round(x), round(y)]


def bilinear(img, x, y):
    dx = x - int(x)
    dy = y - int(y)
    x = int(x)
    y = int(y)
    res = (1 - dx) * (1 - dy) * img[x, y]
    res += dx * (1 - dy) * img[x + 1, y]
    res += (1 - dx) * dy * img[x, y + 1]
    res += dx * dy * img[x + 1, y + 1]

    return res


def bicubica(x, y):
    return (x, y)


def lagrange(x, y):
    return (x, y)


interpolation_methods = {
    "bilinear": bilinear,
    "bicubica": bicubica,
    "proximo": proximo,
    "lagrange": lagrange,
}


if __name__ == "__main__":
    rotation_degree = args.angulo
    scale_factor = args.escala
    output_dimension = args.dimensao
    interpolation_method = interpolation_methods[args.metodo]
    input_image = args.imagem
    output_image = args.saida

    img = cv2.imread(input_image)

    out = scale_and_rotate_image(
        img, scale_factor, rotation_degree, output_dimension, interpolation_method
    )

    cv2.imwrite(output_image, out)
