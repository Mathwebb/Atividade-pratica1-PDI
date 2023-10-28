from PIL import Image


def marca_fronteira_v4(imagem: Image, modify=False):
    if not modify:
        imagem = imagem.copy()
    for x in range(imagem.width):
        for y in range(imagem.height):
            preto = (0, 0, 0, 255)
            vizinhos = []

            try:
                vizinhos.append(imagem.getpixel((x - 1, y)))
                vizinhos.append(imagem.getpixel((x + 1, y)))
                vizinhos.append(imagem.getpixel((x, y - 1)))
                vizinhos.append(imagem.getpixel((x, y + 1)))
            except IndexError:
                pass

            if imagem.getpixel((x, y)) == (255, 255, 255, 255) and len(vizinhos) == 4:
                for vizinho in vizinhos:
                    if vizinho == preto:
                        imagem.putpixel((x, y), (255, 0, 0, 255))

    for x in range(imagem.width):
        for y in range(imagem.height):
            if imagem.getpixel((x, y)) == (255, 255, 255, 255):
                imagem.putpixel((x, y), (0, 0, 0, 255))

    return imagem


def marca_fronteira_v8(imagem: Image, modify=False):
    if not modify:
        imagem = imagem.copy()
    for x in range(imagem.width):
        for y in range(imagem.height):
            vizinhos = []

            try:
                vizinhos.append(imagem.getpixel((x-1, y)))
                vizinhos.append(imagem.getpixel((x+1, y)))
                vizinhos.append(imagem.getpixel((x, y-1)))
                vizinhos.append(imagem.getpixel((x, y+1)))
                vizinhos.append(imagem.getpixel((x-1, y-1)))
                vizinhos.append(imagem.getpixel((x-1, y+1)))
                vizinhos.append(imagem.getpixel((x+1, y+1)))
                vizinhos.append(imagem.getpixel((x+1, y-1)))
            except IndexError:
                pass

            if imagem.getpixel((x, y)) == (255, 255, 255, 255) and len(vizinhos) == 8:
                for vizinho in vizinhos:
                    if vizinho == (0, 0, 0, 255):
                        imagem.putpixel((x, y), (255, 0, 0, 255))

    for x in range(imagem.width):
        for y in range(imagem.height):
            if imagem.getpixel((x, y)) == (255, 255, 255, 255):
                imagem.putpixel((x, y), (0, 0, 0, 255))

    return imagem


if __name__ == '__main__':
    with Image.open('assets/aviao.png') as image:
        image_v4 = marca_fronteira_v4(image)
        image_v4.save('resultados/folha_marcada_V4.png')
        image_v8 = marca_fronteira_v8(image)
        image_v8.save('resultados/folha_marcada_v8.png')
