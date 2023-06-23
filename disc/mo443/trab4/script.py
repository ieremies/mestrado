import cv2
import numpy as np

# Pontos de origem
points_src = np.array([[37, 51], [342, 42], [485, 467], [73, 380]], dtype=np.float32)

# Pontos de destino
points_dst = np.array([[0, 0], [511, 0], [511, 511], [0, 511]], dtype=np.float32)

matrix = cv2.getPerspectiveTransform(points_src, points_dst)

# Exemplo de aplicação em uma imagem
image = cv2.imread("baboon_perspectiva.png")  # Carregue sua imagem de entrada

# Aplicar a transformação
result = cv2.warpPerspective(
    image, matrix, (512, 512)
)  # (512, 512) é o tamanho da imagem de saída

cv2.imwrite("./out.png", result)

import cv2
import numpy as np


def scale_and_rotate_image(image, scale_factor, angle):
    # Obter a altura e largura da imagem
    height, width = image.shape[:2]

    # Calcular o centro da imagem
    center = (width // 2, height // 2)

    # Definir a matriz de transformação para escala
    scale_matrix = np.array(
        [[scale_factor, 0, 0], [0, scale_factor, 0], [0, 0, 1]], dtype=np.float32
    )

    # Definir a matriz de transformação para rotação
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Aplicar as transformações de escala e rotação
    scaled_image = cv2.warpAffine(image, scale_matrix, (width, height))
    scaled_rotated_image = cv2.warpAffine(
        scaled_image, rotation_matrix, (width, height)
    )

    return scaled_rotated_image


# Carregar a imagem
image = cv2.imread(
    "baboon_perspectiva.png"
)  # Substitua pelo caminho e nome da sua imagem

# Definir o fator de escala e o ângulo de rotação
scale_factor = 0.8  # Fator de escala: 0.8 significa 80% do tamanho original
angle = 30.0  # Ângulo de rotação: 30 graus no sentido anti-horário

# Aplicar as transformações
transformed_image = scale_and_rotate_image(image, scale_factor, angle)

# Exibir a imagem original e a transformada
cv2.imwrite("./out.png", transformed_image)
