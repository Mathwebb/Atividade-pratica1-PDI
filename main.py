from PIL import Image
# Documentação pillow: https://pillow.readthedocs.io/en/stable/index.html


def inverte_imagem(imagem: Image, modify=False):
    if not modify:
        imagem = imagem.copy()
    for line in range(imagem.width):
        for column in range(imagem.height):
            pixel = imagem.getpixel((line, column))
            if pixel == 0:
                imagem.putpixel((line, column), 1)
            else:
                imagem.putpixel((line, column), 0)
    return imagem


def marca_fronteira_v4(imagem: Image, modify=False):
    if not modify:
        imagem = imagem.copy()
    for line in range(imagem.width):
        for column in range(imagem.height):
            preto = 0
            vizinhos = []

            try:
                vizinhos.append(imagem.getpixel((line - 1, column)))
                vizinhos.append(imagem.getpixel((line + 1, column)))
                vizinhos.append(imagem.getpixel((line, column - 1)))
                vizinhos.append(imagem.getpixel((line, column + 1)))
            except IndexError as error:
                pass

            if imagem.getpixel((line, column)) == 1 and len(vizinhos) == 4:
                for vizinho in vizinhos:
                    if vizinho == preto:
                        imagem.putpixel((line, column), 125)

    for line in range(imagem.width):
        for column in range(imagem.height):
            if imagem.getpixel((line, column)) == 1:
                imagem.putpixel((line, column), 0)

    return imagem


def marca_fronteira_v8(imagem: Image, modify=False):
    if not modify:
        imagem = imagem.copy()
    for line in range(imagem.width):
        for column in range(imagem.height):
            vizinhos = []

            try:
                vizinhos.append(imagem.getpixel((line-1, column)))
                vizinhos.append(imagem.getpixel((line+1, column)))
                vizinhos.append(imagem.getpixel((line, column-1)))
                vizinhos.append(imagem.getpixel((line, column+1)))
                vizinhos.append(imagem.getpixel((line-1, column-1)))
                vizinhos.append(imagem.getpixel((line-1, column+1)))
                vizinhos.append(imagem.getpixel((line+1, column+1)))
                vizinhos.append(imagem.getpixel((line+1, column-1)))
            except IndexError as error:
                pass

            if imagem.getpixel((line, column)) == 1 and len(vizinhos) == 8:
                for vizinho in vizinhos:
                    if vizinho == 0:
                        imagem.putpixel((line, column), 125)

    for line in range(imagem.width):
        for column in range(imagem.height):
            if imagem.getpixel((line, column)) == 1:
                imagem.putpixel((line, column), 0)

    return imagem


def calcula_histograma(imagem: Image):
    histograma = []

    for i in range(256):
        histograma.append(0)

    for column in range(imagem.width):
        for line in range(imagem.height):
            intensidade = imagem.getpixel((line, column))
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
            fda.append(probabilidade_pixel * 256)
        else:
            fda.append(probabilidade_pixel * 256 + fda[numero_pixel-1])

    return fda


def equaliza(imagem: Image, modify=False):
    if not modify:
        imagem = imagem.copy()
    fda = calcula_fda(imagem)
    fda_round = []

    for intensidade in fda:
        fda_round.append(round(intensidade))

    for line in range(imagem.width):
        for column in range(imagem.height):
            intensidade_pixel = imagem.getpixel((line, column))
            imagem.putpixel((line, column), fda_round[intensidade_pixel])

    return imagem


if __name__ == '__main__':
    with Image.open('assets/aviao.png') as imagem:
        imagem = inverte_imagem(imagem)
        imagem.save('resultados/aviao_invertido.png')
        imagem_v4 = marca_fronteira_v4(imagem)
        imagem_v4.save('resultados/folha_marcada_V4.png')
        imagem_v8 = marca_fronteira_v8(imagem)
        imagem_v8.save('resultados/folha_marcada_v8.png')

    # with Image.open('assets/lena_gray.bmp') as imagem:
    #     equaliza(imagem)
    #     imagem.show()
    #     equaliza(imagem)
    #     imagem.show()
