from PIL import Image
import matplotlib.pyplot as plt


def calcula_histograma(imagem: Image):
    histograma = []

    for i in range(256):
        histograma.append(0)

    for x in range(imagem.width):
        for y in range(imagem.height):
            intensidade = imagem.getpixel((x, y))
            histograma[intensidade] += 1

    return histograma


def calcula_fdp(imagem: Image):
    histograma = calcula_histograma(imagem)
    tam_imagem = imagem.width * imagem.height
    fdp = []  # função de distribuição de probabilidades

    for pixel_count in histograma:
        fdp.append(pixel_count/tam_imagem)
    return fdp


def calcula_fda(imagem: Image):
    histograma = calcula_histograma(imagem)
    fdp = calcula_fdp(imagem)
    fda = []  # função de distribuição acumulada

    for numero_pixel in range(0, len(histograma)):
        probabilidade_pixel = fdp[numero_pixel]
        if numero_pixel == 0:
            fda.append(probabilidade_pixel * 255)
        else:
            fda.append(probabilidade_pixel * 255 + fda[numero_pixel-1])

    return fda


def grafico_histograma(imagem):
    histogram = calcula_histograma(imagem)

    x = []
    for i in range(256):
        x.append(i)
    y = histogram

    fig, ax = plt.subplots()

    ax.stem(x, y)


def grafico_fdp(imagem):
    fdp = calcula_fdp(imagem)

    x = []
    for i in range(256):
        x.append(i)
    y = fdp

    fig, ax = plt.subplots()

    ax.stem(x, y)


def grafico_fda(imagem):
    fda = calcula_fda(imagem)

    x = []
    for i in range(256):
        x.append(i)
    y = fda

    fig, ax = plt.subplots()

    ax.stem(x, y)


if __name__ == '__main__':
    with Image.open('assets/lena_gray.bmp') as image:
        print('Histograma: ', calcula_histograma(image))
        print('fdp: ', calcula_fdp(image))
        print('fda: ', calcula_fda(image))
        grafico_histograma(image)
        grafico_fdp(image)
        grafico_fda(image)
        plt.show()
