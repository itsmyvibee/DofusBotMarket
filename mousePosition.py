
"""
Método que devolve a posição atual do cursor (x, y)
"""

import win32api

def getMousePosition():
    x, y = win32api.GetCursorPos()
    #print('x: {}    y: {}'.format(x, y))
    return x, y
