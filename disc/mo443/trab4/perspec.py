import numpy as np
import cv2

# pontos de origem e destino
src = np.float32([[37, 51], [342, 42], [485, 467], [73, 380]])
dest = np.float32([[0, 0], [511, 0], [511, 511], [0, 511]])

# Calcular a matriz de transformação
M = cv2.getPerspectiveTransform(src, dest)

image = cv2.imread("img/baboon_perspectiva.png")

output_image = cv2.warpPerspective(image, M, (512, 512))

cv2.imwrite("./out.png", output_image)
