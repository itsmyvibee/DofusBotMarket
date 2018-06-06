import win32api
from time import sleep
import mousePosition



#Virtual key code
# VK_LBUTTON 0x01  LeftClick
# VK_RBUTTON 0x02  RightClick
# Retorno do método: return < 0 caso o botão seja apertado || return == 0 tecla desmarcada || return == 1 tecla desativada
def getPosicaoDoClick():

    """
    Verifica a posição em que houve um clique no mouse, clicks esses que serão utilizados para criar um retângulo ficticio para leitura de dados pelo OCR.

    :return: pos x, pos y   do click
    """


    leftClickBefore = win32api.GetKeyState(0x01)
    rightClickBefore = win32api.GetKeyState(0x02)

    while 1:
        leftClick = win32api.GetKeyState(0x01)
        rightClick = win32api.GetKeyState(0x02)

        if leftClick != leftClickBefore:
            leftClickBefore = leftClick
            if leftClick < 0 or leftClick == 1:
                x, y = mousePosition.getMousePosition()
                #print('Clique com botão esquerdo na posição x:{}  y:{}'.format(x, y))
                return x, y


        if rightClick != rightClickBefore:
            rightClickBefore = rightClick
            if rightClick < 0 or leftClick == 1:
                x, y = mousePosition.getMousePosition()
                #print('Clique com botão direto na posição x:{}  y:{}'.format(x, y))
                return x, y

        sleep(0.2)


#Método para criar area de click do botao comprar
def getPositionBotaoComprar():
    print('\tClick com botão direito no botão comprar.')
    x, y = getPosicaoDoClick()
    print('\n\tPosição do botão comprar: ({}, {})'.format(x, y))
    win32api.Beep(800, 150)
    win32api.MessageBeep()
    return x, y