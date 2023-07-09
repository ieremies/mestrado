import numpy as np
import cv2
from math import ceil
from arg_parser import args


def scale_and_rotate_image(image, scale_factor, angle, dim, interp):
    # converter angle para radianos
    angle = np.deg2rad(angle)

    # Criar uma imagem com a dimensão dim em preto
    res = np.zeros((dim[1], dim[0], 3), np.uint8)

    # O centro da imagem de saída
    center = (dim[1] // 2, dim[0] // 2)

    # O centro da imagem de entrada
    center_in = (image.shape[1] // 2, image.shape[0] // 2)

    for x in range(dim[0]):
        for y in range(dim[1]):
            # aplicar a escala baseado na distância do pixel ao
            # centro da imagem
            coord = (
                (y - center[0]) / scale_factor,
                (x - center[1]) / scale_factor,
            )
            # aplicar a rotação utilizando a formula da inversa da
            # rotação:
            # x' = cos(a)x + sin(a)y e
            # y' = - sin(a)x + cos(a)y
            coord = (
                coord[0] * np.cos(angle) + coord[1] * np.sin(angle),
                coord[1] * np.cos(angle) - coord[0] * np.sin(angle),
            )
            # transladar de volta ao centro
            coord = (
                coord[0] + center_in[0],
                coord[1] + center_in[1],
            )
            # utilizamos o método de interpolação para obter o pixel
            res[y, x] = interp(image, *coord)

    return res


def proximo(img, x, y):
    x = round(x)
    y = round(y)
    if x >= img.shape[0]:
        return 0
    if y >= img.shape[1]:
        return 0
    return img[x, y]


def bilinear(img, x, y):
    dx = x - int(x)
    dy = y - int(y)
    x = int(x) if int(x) < img.shape[0] else img.shape[0] - 1
    y = int(y) if int(y) < img.shape[1] else img.shape[1] - 1
    x1 = x + 1 if x + 1 < img.shape[0] else x
    y1 = y + 1 if y + 1 < img.shape[1] else y
    res = (1 - dx) * (1 - dy) * img[x, y]
    res += dx * (1 - dy) * img[x1, y]
    res += (1 - dx) * dy * img[x, y1]
    res += dx * dy * img[x1, y1]

    return res


def bicubica(img, x, y):
    pass


def lagrange(x, y):
    pass


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
