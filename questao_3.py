from PIL import Image


def calcula_histograma(imagem: Image):
    histograma = []

    for i in range(256):
        histograma.append(0)

    for x in range(imagem.width):
        for y in range(imagem.height):
            intensidade = imagem.getpixel((x, y))
            histograma[intensidade] += 1

    return histograma


def calcula_fdp(imagem: Image, histograma=None, tam_imagem=None):
    if histograma is None:
        histograma = calcula_histograma(imagem)
    if tam_imagem is None:
        tam_imagem = imagem.width * imagem.height

    fdp = []  # função de distribuição de probabilidades

    for pixel_count in histograma:
        fdp.append(pixel_count/tam_imagem)
    return fdp


def calcula_fda(imagem: Image, histograma=None, fdp=None):
    if histograma is None:
        histograma = calcula_histograma(imagem)
    if fdp is None:
        fdp = calcula_fdp(imagem, histograma)

    fda = []  # função de distribuição acumulada

    for numero_pixel in range(0, len(histograma)):
        probabilidade_pixel = fdp[numero_pixel]
        if numero_pixel == 0:
            fda.append(probabilidade_pixel * 255)
        else:
            fda.append(probabilidade_pixel * 255 + fda[numero_pixel-1])

    return fda


def equaliza(imagem: Image, modify=False):
    if not modify:
        imagem = imagem.copy()
    fda = calcula_fda(imagem)
    fda_round = []

    for intensidade in fda:
        fda_round.append(round(intensidade))

    for x in range(imagem.width):
        for y in range(imagem.height):
            intensidade_pixel = imagem.getpixel((x, y))
            imagem.putpixel((x, y), fda_round[intensidade_pixel])

    return imagem

if __name__ == '__main__':
    with Image.open('assets/lena_gray.bmp') as image:
        equaliza(image, True)
        image.show()
        image.save('resultados/lena_gray_equalizada.bmp')
        print('Histograma da primeira equalizacao: ', calcula_histograma(image))
        equaliza(image, True)
        image.show()
        image.save('resultados/lena_gray_equalizada_2x.bmp')
        print('Histograma da segunda equalizacao: ', calcula_histograma(image))

    with Image.open('assets/image1.png') as image:
        equaliza(image, True)
        image.show()
        image.save('resultados/image1_equalizada.png')
        print('Histograma da primeira equalizacao: ', calcula_histograma(image))
        equaliza(image, True)
        image.show()
        image.save('resultados/image1_equalizada_2x.png')
        print('Histograma da segunda equalizacao: ', calcula_histograma(image))
