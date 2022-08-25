from PIL import Image
from math import log
from questao_2 import grafico_histograma
import matplotlib.pyplot as plt


def transformacao_linear(imagem: Image, c, b, modify=False):
    if not modify:
        imagem = imagem.copy()
    for x in range(imagem.width):
        for y in range(imagem.height):
            intensidade_pixel = imagem.getpixel((x, y))
            imagem.putpixel((x, y), round(c * intensidade_pixel + b))

    return imagem


def transformacao_logaritmica(imagem: Image, c, modify=False):
    if not modify:
        imagem = imagem.copy()
    for x in range(imagem.width):
        for y in range(imagem.height):
            intensidade_pixel = imagem.getpixel((x, y))
            imagem.putpixel((x, y), round(c * log(intensidade_pixel + 1, 2)))

    return imagem


def transformacao_potencia(imagem: Image, c, gama, modify=False):
    if not modify:
        imagem = imagem.copy()
    for x in range(imagem.width):
        for y in range(imagem.height):
            intensidade_pixel = imagem.getpixel((x, y))
            intensidade_pixel = c * (intensidade_pixel ** gama)
            imagem.putpixel((x, y), round(intensidade_pixel))

    return imagem


if __name__ == '__main__':
    with Image.open('assets/lena_gray.bmp') as image:
        image.save('assets/lena_gray.png')
        # imagem_lin = transformacao_linear(image, 0.2, 80)
        # imagem_lin.show()
        # imagem_lin.save('resultados/lena_gray_linear.png')
        # grafico_histograma(imagem_lin)

        # imagem_log = transformacao_logaritmica(image, 30)
        # imagem_log.show()
        # imagem_log.save('resultados/lena_gray_log.png')
        # grafico_histograma(imagem_log)

        imagem_pot = transformacao_potencia(image, 1, 0.6)
        imagem_pot.show()
        imagem_pot.save('resultados/lena_gray_pot.png')
        grafico_histograma(imagem_pot)

        plt.show()
