#TODO Analisar preço > Clicar no lote > clicar no botao comprar > e dar enter
from win32api import mouse_event, keybd_event, SetCursorPos
import win32con
from time import sleep

def analisarPreco(precoOCR, carteira):
    if int(precoOCR) < int(carteira):
        #print('Compra permitida.')
        return True

    else:
        print('Compra não foi permitida... Você possivelmente não possui dinheiro o suficiente')
        return False #O false vai tirar do loop de comprar esse lote e passar para o proximo.


def fazerCompra(lote, coordenadasLotes, coordenadaBotaoComprar):

    xBotao = coordenadaBotaoComprar[0]
    yBotao = coordenadaBotaoComprar[1]

    #Click no lote
    if lote == 1:
        x = int(coordenadasLotes[0][1][0])
        y = int(coordenadasLotes[0][1][1])
    elif lote == 10:
        x = int(coordenadasLotes[1][1][0])
        y = int(coordenadasLotes[1][1][1])
    elif lote == 100:
        x = int(coordenadasLotes[2][1][0])
        y = int(coordenadasLotes[2][1][1])

    #Click no lote
    SetCursorPos((x, y))
    mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    sleep(0.05)
    mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    sleep(0.05)

    #Click no Comprar
    SetCursorPos((xBotao, yBotao))
    mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, xBotao, yBotao, 0, 0)
    sleep(0.05)
    mouse_event(win32con.MOUSEEVENTF_LEFTUP, xBotao, yBotao, 0, 0)
    sleep(0.05)

    sleep(0.05)

    #Enter para realizar compra
    keybd_event(0x0D, 0, 0, 0)
    sleep(0.05)
    keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)
    sleep(0.2)
