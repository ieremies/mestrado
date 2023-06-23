"""
prog [-a ângulo]
     [-e fator de escala]
     [-d largura altura]
     [-m método de interpolação]
     [-i imagem entrada]
     [-o imagem saída]

Onde:
-a ângulo de rotação medido em graus no sentido anti-horário
-e fator de escala
-d dimens~ao da imagem de saída em pixels
-m método de interpolação utilizado
-i imagem de entrada no formato PNG
-o imagem de sa´ıda no formato PNG (após transformação)
"""

import argparse

parser = argparse.ArgumentParser(description="Processa imagens")
parser.add_argument(
    "-a",
    "--angulo",
    type=float,
    help="ângulo de rotação medido em graus no sentido anti-horário",
    default=0.0,
)
parser.add_argument("-e", "--escala", type=float, help="fator de escala", default=1.0)
parser.add_argument(
    "-d", "--dimensao", type=int, nargs=2, help="dimensão da imagem de saída em pixels"
)
parser.add_argument("-m", "--metodo", type=str, help="método de interpolação utilizado")
parser.add_argument("-i", "--imagem", type=str, help="imagem de entrada no formato PNG")
parser.add_argument(
    "-o",
    "--saida",
    type=str,
    help="imagem de saída no formato PNG (após transformação)",
)
args = parser.parse_args()
