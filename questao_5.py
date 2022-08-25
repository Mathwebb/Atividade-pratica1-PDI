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


def calcula_fdp(imagem: Image = None, histograma=None):

    fdp = []  # função de distribuição de probabilidades
    tam_imagem = 0

    if imagem is not None:
        if histograma is None:
            histograma = calcula_histograma(imagem)

        tam_imagem = imagem.width * imagem.height

        for pixel_count in histograma:
            fdp.append(pixel_count/tam_imagem)
        return fdp
    elif histograma is not None:
        for pixel_count in histograma:
            tam_imagem += pixel_count

        for pixel_count in histograma:
            fdp.append(pixel_count/tam_imagem)
        return fdp


def calcula_fda(imagem: Image = None, histograma=None, fdp=None):

    fda = []  # função de distribuição acumulada

    if imagem is not None:
        if histograma is None:
            histograma = calcula_histograma(imagem)
        if fdp is None:
            fdp = calcula_fdp(imagem, histograma)

        for numero_pixel in range(0, len(histograma)):
            probabilidade_pixel = fdp[numero_pixel]
            if numero_pixel == 0:
                fda.append(probabilidade_pixel * 255)
            else:
                fda.append(probabilidade_pixel * 255 + fda[numero_pixel-1])

        return fda
    elif histograma is not None:
        if fdp is None:
            fdp = calcula_fdp(histograma=histograma)

        for numero_pixel in range(0, len(histograma)):
            probabilidade_pixel = fdp[numero_pixel]
            if numero_pixel == 0:
                fda.append(probabilidade_pixel * 255)
            else:
                fda.append(probabilidade_pixel * 255 + fda[numero_pixel - 1])

        return fda


def equaliza(imagem: Image = None, histograma=None, modify=False):
    if imagem is not None:
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
    elif histograma is not None:
        fda = calcula_fda(histograma=histograma)
        fda_round = []
        histograma_result = []
        for i in range(len(histograma)):
            histograma_result.append(0)

        for intensidade in fda:
            fda_round.append(round(intensidade))

        for i in range(len(histograma_result)):
            histograma_result[fda_round[i]] += histograma[i]

        return fda_round


def especificacao(imagem: Image, histograma_especificado: list, modify=False):
    if not modify:
        imagem = imagem.copy()

    imagem = equaliza(imagem)
    map_especif = equaliza(histograma=histograma_especificado)
    map_equal = equaliza(histograma=calcula_histograma(imagem))
    fdp_equal = calcula_fdp(imagem)
    map_final = []

    for i in range(len(histograma_especificado)):
        map_final.append(None)

    for i in range(len(histograma_especificado)):
        for t in range(len(histograma_especificado)):
            if map_final[t] is None and fdp_equal[i] > 0:
                if map_especif[t] == map_equal[i]:
                    map_final[i] = map_equal[t]
                    break
                if map_especif[t] > map_equal[i]:
                    map_final[i] = map_equal[t-1]
                    break

    for x in range(imagem.width):
        for y in range(imagem.height):
            intensidade_pixel = imagem.getpixel((x, y))
            if map_final[intensidade_pixel] is not None:
                imagem.putpixel((x, y), map_final[intensidade_pixel])

    return imagem


def grafico_fdp(imagem):

    fdp = calcula_fdp(imagem)

    x = []
    for i in range(256):
        x.append(i)
    y = fdp

    fig, ax = plt.subplots()

    ax.stem(x, y)


if __name__ == '__main__':
    image1 = Image.open('assets/image1.png')
    lena_gray = Image.open('assets/lena_gray.bmp')
    grafico_fdp(lena_gray)
    imagem_final = especificacao(image1, calcula_histograma(lena_gray))
    grafico_fdp(equaliza(image1))
    grafico_fdp(imagem_final)
    imagem_final.show()
    imagem_final.save('resultados/image1_especificada.png')

    plt.show()
