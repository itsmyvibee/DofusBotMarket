from PIL import ImageGrab
from win32api import MessageBeep, Beep, MessageBox
import time
from PIL import Image
import pytesseract as ocr
import detectMouseClick             #Import do detectMouseClick.py
import numpy as np
import cv2
ocr.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract' #TODO TXT para colocar o caminho do tesseractCMD

#Método para criar area de leitura dos preços dos lotes
def getRetangulos():
    """
   Cria as áreas de leitura para os lotes x1, x10, x100

   :return: Matriz com todos os 3 dados, contendo (lote, pos1, pos2)
    """

    retangulos = []

    i = 1

    while i <= 100:
        time.sleep(1)
        print('\tClique no ponto de construção 1 para lote de x{}:'.format(i))
        pos1 = detectMouseClick.getPosicaoDoClick()         #Recebe os parametros x , y em uma tupla
        print('\tPosição 1: ({}, {})'.format(pos1[0], pos1[1]))
        Beep(800, 150)
        time.sleep(1)

        print('\tClique no ponto de construção 2 para lote de x{}:'.format(i))
        pos2 = detectMouseClick.getPosicaoDoClick()         #Recebe os parametros x , y em uma tupla
        print('\tPosição 2: ({}, {})'.format(pos2[0], pos2[1]))
        Beep(800, 150)

        construcao = [i, pos1, pos2]                        #Faz matriz com o index(lote), (pos1), (pos2)
        retangulos.append(construcao)
        print('\n')

        i *= 10

    #print('Posições dos lotes: ', retangulos)
    print('\tPosição dos lotes recebida com sucesso!')
    MessageBeep()
    return retangulos

#Método para criar area de leitura da carteira
def getRetanguloSeusKamas():

    print('\n\tDefinindo posição da sua carteira de Kamas: ')

    time.sleep(1)
    print('\tClique no ponto de construção 1 para seus Kamas:')
    pos1 = detectMouseClick.getPosicaoDoClick()             # Recebe os parametros x , y em uma tupla
    print('\tPosição 1: ({}, {})'.format(pos1[0], pos1[1]))
    Beep(800, 150)

    time.sleep(1)
    print('\tClique no ponto de construção 2 para seus Kamas:')
    pos2 = detectMouseClick.getPosicaoDoClick()             # Recebe os parametros x , y em uma tupla
    print('\tPosição 2: ({}, {})'.format(pos2[0], pos2[1]))
    Beep(800, 150)
    posicaoKamas = [pos1, pos2]

    #print('Posição da carteira de kamas: ', posicaoKamas)
    print('\n\tPosição da carteira recebida com sucesso!')
    MessageBeep()
    return posicaoKamas

#Métodos de leitura
#1.0 Método Ler carteira
def lerCarteira(coordenadas):

    screen = ImageGrab.grab(bbox=(int(coordenadas[0][0]),   #X1
                            int(coordenadas[0][1]),         #Y1
                            int(coordenadas[1][0]),         #X2
                            int(coordenadas[1][1])))        #Y2

    string = aprimorarImagem_RetornarTexto(screen)
    return string

#2.0 Métodos Ler Lotes
#Matriz [[lote, (x1, y1), (x2, y2)], [...], [...]]
def lerLote1(coordenadasLotes):

    x1 = int(coordenadasLotes[0][1][0])
    y1 = int(coordenadasLotes[0][1][1])
    x2 = int(coordenadasLotes[0][2][0])
    y2 = int(coordenadasLotes[0][2][1])

    screen = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    string = aprimorarImagem_RetornarTexto(screen)
    return string

def lerLote10(coordenadasLotes):

    x1 = int(coordenadasLotes[1][1][0])
    y1 = int(coordenadasLotes[1][1][1])
    x2 = int(coordenadasLotes[1][2][0])
    y2 = int(coordenadasLotes[1][2][1])

    screen = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    string = aprimorarImagem_RetornarTexto(screen)
    return string

def lerLote100(coordenadasLotes):

    x1 = int(coordenadasLotes[2][1][0])
    y1 = int(coordenadasLotes[2][1][1])
    x2 = int(coordenadasLotes[2][2][0])
    y2 = int(coordenadasLotes[2][2][1])

    screen = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    string = aprimorarImagem_RetornarTexto(screen)
    return string

#3.0 Método Aprimorar imagem para aumentar efetividade da leitura
def aprimorarImagem_RetornarTexto(imagem):
    """
    Método utilizado para melhorar a imagem para leitura do OCR
    :param imagem: imagem que ira ser aprimorada
    :return: retorna imagem aprimorada
    """
    # 3.1 Aumentar tamanho da imagem
    #baseheight = 60 #PROBLEMAS COM 8
    #baseheight = 55
    #hpercent = (baseheight / float(imagem.size[1]))
    #wsize = int((float(imagem.size[0]) * float(hpercent)))
    #imgTratada = imagem.resize((wsize, baseheight), Image.ANTIALIAS)
    #imgTratada.show()  # Show

    baseheight = list(range(80, 84))

    dado1 = None
    cd1 = 0
    cd2 = 0
    dado2 = None

    for i in baseheight:
        hpercent = (i / float(imagem.size[1]))
        wsize = int((float(imagem.size[0]) * float(hpercent)))
        imgTratada = imagem.resize((wsize, i), Image.ANTIALIAS)
        s = dicionarioDeManutencao(ocr.image_to_string(imgTratada))

        if dado1 == None:
            dado1 = s
            cd1 += 1
        if dado1 == s:
            cd1 += 1
        elif dado2 == None:
            dado2 = s
            cd2 += 1
        elif dado2 == s:
            cd2 += 1

        #print('Base {}: {}'.format(i, s))
    #print('\nDado 1: {} > {}x\nDado 2: {} > {}x'.format(dado1, cd1, dado2, cd2))
    if cd2 > cd1:
        return dado2
    elif cd2 == cd1:
        dado1 = int(dado1)
        dado2 = int(dado2)
        if dado1 > dado2:
            return dado1
        else:
            return dado2
    else:
        return dado1


    """
    # 3.2 Converter para arrays RGB
    imgTratada = imgTratada.convert('RGB')
    npimagem = np.asarray(imgTratada).astype(np.uint8)

    npimagem[:, :, 0] = 0  # Zerando canal Red
    npimagem[:, :, 2] = 0  # Zerando canal Blue

    im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY)  # Atribuindo escala em cinza

    # aplicação da truncagem binária para a intensidade
    # pixels de intensidade de cor abaixo de 127 serão convertidos para 0 (PRETO)
    # pixels de intensidade de cor acima de 127 serão convertidos para 255 (BRANCO)
    # A atrubição do THRESH_OTSU incrementa uma análise inteligente dos nivels de truncagem
    ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
    imageComplete = Image.fromarray(thresh)

    imageComplete.show()
    """

def dicionarioDeManutencao(stringLida):

    x = str(stringLida)
    x = x.upper()
    x = x.replace(' ', '')
    x = x.replace('K', '')
    x = x.replace('S', '5')
    x = x.replace('O', '0')
    x = x.replace('I', '1')
    x = x.replace('L', '1')
    x = x.replace('E', '6')
    x = x.replace('B', '8')
    x = x.replace('.', '')
    x = x.replace('-', '')
    x = x.replace('‘', '')
    x = x.replace('A', '4')
    x = x.replace('<', '')
    x = x.replace('|', '')
    x = x.replace('(', '')
    x = x.replace('«', '')
    x = x.replace('—', '')
    x = x.replace('~', '')
    x = x.replace('{', '')
    x = x.replace('?', '')
    x = x.replace('C', '0')
    x = x.replace('_', '')

    if x == '':
        x = '999999999999999999'

    return x

def testeOCR():
    img = Image.open('palavraTeste.jpg')
    print(ocr.image_to_string(img))

