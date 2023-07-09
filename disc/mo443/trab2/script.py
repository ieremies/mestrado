import cv2
import numpy as np
import matplotlib.pyplot as plt
from funcs import *

# Read all images in img folder
imgs = ["baboon", "fiducial", "monarch", "peppers", "retina", "sonnet", "wedge"]

# Métodos globais
methods = [lin_global, otsu]
for file in imgs:
    for method in methods:
        # Read image
        img = cv2.imread("img/" + file + ".pgm", 0)

        # Apply method
        img = method(img)

        cv2.imwrite(f"out/{file}-{method.__name__}.pgm", img)

importante = [
    ("baboon", bernsen),
    ("sonnet", niblack),
    ("wedge", sauvola),
    ("peppers", contraste),
    ("peppers", media),
    ("peppers", mediana),
]


for file, method in importante:
    # Read image
    img = cv2.imread("img/" + file + ".pgm", 0)

    # Apply method
    img = local(img, method)

    cv2.imwrite(f"out/{file}-{method.__name__}.pgm", img)


# Métodos locais
methods = [bernsen, niblack, sauvola, phansalskar, contraste, media, mediana]
color = ["red", "green", "yellow", "black", "purple", "orange", "pink", "gray"]
for file in imgs:
    # Read image
    img = cv2.imread("img/" + file + ".pgm", 0)
    # hist, _ = np.histogram(img, bins=256, range=[0, 255])
    # plt.hist(hist, bins=256, range=[0, 255], histtype="stepfilled", color="blue")

    for i in range(len(methods)):
        # Apply method
        res = local(img, methods[i])

        # calcular o histograma do resultado, baseado no valor inicial
        # hist = np.zeros(256)
        # for x in range(img.shape[0]):
        #     for y in range(img.shape[1]):
        #         if res[x][y] == 255:
        #             hist[img[x][y]] += 1
        # histograma
        # plt.hist(
        #     hist,
        #     bins=256,
        #     range=[0, 255],
        #     histtype="stepfilled",
        #     color=color[i],
        #     alpha=0.5,
        #     label=methods[i].__name__,
        # )

        cv2.imwrite(f"out/{file}-{methods[i].__name__}.pgm", res)
    # plt.savefig(f"hist/{file}.png")
