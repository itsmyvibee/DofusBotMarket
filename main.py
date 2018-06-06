import ocr as marketDofusBot
import detectMouseClick
from time import sleep
import robotActions


def showMenu():
    """
    Monta o menu para prompt

    :return:
    """

    print('\t{:=^30}'.format(' Dofus Bot Buy '))

    print('\n\tMenu')
    print('\t[1] Create new scale and new save')
    print('\t[2] Use saved scale')
    print('\t[3] Test OCR reader')
    print('\t[4] Exit')
    op = input('\tOpção: ')

    return op

def criarMapasDePosicoes():
    """
    Método que irá fazer a criação dos retangulos de área de leitura, áreas que serão utilizadas para a atuação do OCR

    :return: Matrizes de posição
    """

    posicoesLotes = marketDofusBot.getRetangulos()                      # Criar posições dos lotes 1x 10x 100x
    posicaoCarteira = marketDofusBot.getRetanguloSeusKamas()            # Criar posição da carteira kamas inventário
    posicaoBotaoComprar = detectMouseClick.getPositionBotaoComprar()    # Cria posição do botão comprar para efetuar clicks do bot
    return posicoesLotes, posicaoCarteira, posicaoBotaoComprar

    # Apresentar as posições recebidas
    # print('=-'*22)
    # print(f'Posição dos lotes: \nx{posicoesLotes[0][0]}\t\t{posicoesLotes[0][1]} {posicoesLotes[0][2]}\nx{posicoesLotes[1][0]}\t\t{posicoesLotes[1][1]} {posicoesLotes[1][2]}'
    #      f'\nx{posicoesLotes[2][0]}\t{posicoesLotes[2][1]} {posicoesLotes[2][2]}')
    #
    # print('\nPosição da carteira: {} {}'.format(posicaoCarteira[0], posicaoCarteira[1]))
    # print('=-'*22)

def executar(posicoesLotes, posicaoCarteira, posicaoBotaoComprar):
    """
    Vai receber todas as possicoes e repassar para os métodos de avaliação e de ação de compra do bot...
    Também precisa ter o preço, nome e lote para poder realizar as ações;

    :param posicoesLotes:
    :param posicaoCarteira:
    :param posicaoBotaoComprar:
    :return:
    """

    #Execução
    #TODO Fazer esse recebimento via dados .txt
    precoMaximoLote1 = int(input('\tPreço maximo da unidade: '))
    precoMaximoLote10 = precoMaximoLote1 * 10
    precoMaximoLote100 =  precoMaximoLote1 * 100
    print('\tPreço max apurado: x1: {} K   x10: {} K   x100: {} K'.format(precoMaximoLote1, precoMaximoLote10, precoMaximoLote100))

    go = True
    lote = 1

    while go:
        sleep(1)

        #Qual lote avaliar? x1, x10, x100?
        if lote == 1:
            precoLote = int(marketDofusBot.lerLote1(posicoesLotes))
            precoMaximo = precoMaximoLote1
            if precoLote >= precoMaximoLote1:
                lote = 10
                print('\tGoing lote 10')
                continue

        elif lote == 10:
            precoLote = int(marketDofusBot.lerLote10(posicoesLotes))
            precoMaximo = precoMaximoLote10
            if precoLote >= precoMaximoLote10:
                lote = 100
                print('\tGoing lote 100')
                continue

        elif lote == 100:
            precoLote = int(marketDofusBot.lerLote100(posicoesLotes))
            precoMaximo = precoMaximoLote100
            if precoLote >= precoMaximoLote100:
                print('\tMudar o item...')
                go = False
                continue

        carteira = marketDofusBot.lerCarteira(posicaoCarteira)

        #print('Preço lote: {} K'.format(precoLote))

        Boolean = robotActions.analisarPreco(precoLote, carteira) #Preço maximo, preco lote, carteira

        if Boolean:
            robotActions.fazerCompra(lote, posicoesLotes, posicaoBotaoComprar) #Lote que irá analisar, posicaolotes, posicaobotaocomprar
            #sleep(0.3)
        else:
            break

    #TODO Verifica preço e efetuar compra
    #TODO Quando for necessario trocar o item que o bot irá operar, da uma pausa para evitar leitura atrasada e errada

def testeOCR(posicoesLotes, posicaoCarteira):
    """
    Teste apenas para verificar como anda o processo de leitura do OCR

    :param posicoesLotes:
    :param posicaoCarteira:
    :return:
    """
    try:
        while 1:
            x1 = marketDofusBot.lerLote1(posicoesLotes)
            x10 = marketDofusBot.lerLote10(posicoesLotes)
            x100 = marketDofusBot.lerLote100(posicoesLotes)
            c = marketDofusBot.lerCarteira(posicaoCarteira)

            print('\n\tLote x1: {}\n\tLote x10: {}\n\tLote x100: {}\n\tCarteira: {}'.format(x1, x10, x100, c))

    except:
        print('Error. Houve algum problema com os blocos de leitura OCR.')

def main():
    """
    Método principal... Aquele que chama todos os outros...
    :return:
    """

    #Variaveis
    posicoesLotes = []
    posicaoCarteira = []
    posicaoBotaoComprar = []

    go = True
    while go:

        opcao = showMenu()

        #Calibra novo mapa
        if opcao == '1':
            posicoesLotes, posicaoCarteira, posicaoBotaoComprar = criarMapasDePosicoes()
            save = open('saveMap.txt', 'w')
            save.write(str(posicoesLotes) + '\n')
            save.write(str(posicaoCarteira) + '\n')
            save.write(str(posicaoBotaoComprar) + '\n')
            save.close()
            #go = False
            executar(posicoesLotes, posicaoCarteira, posicaoBotaoComprar)

        #Carrega mapa
        elif opcao == '2':
            try:
                arquivo = open('saveMap.txt', 'r')
                save = arquivo.readlines()
                posicoesLotes = eval(save[0])
                posicaoCarteira = eval(save[1])
                posicaoBotaoComprar = eval(save[2])
                arquivo.close()
                #go = False
                executar(posicoesLotes, posicaoCarteira, posicaoBotaoComprar)

            except:
                print('Não foi encontrado um arquivo de save válido.')

        #Só para testeOCR
        elif opcao == '3':
            op1 = (input('\tDeseja usar um saveMap [1] Sim  [2] Não ? '))
            if op1 == '1':
                try:
                    arquivo = open('saveMap.txt', 'r')
                    save = arquivo.readlines()
                    posicoesLotes = eval(save[0])
                    posicaoCarteira = eval(save[1])
                    posicaoBotaoComprar = eval(save[2])
                    arquivo.close()
                except:
                    print('Não foi encontrado um arquivo de save válido.')

            else:
                posicoesLotes, posicaoCarteira, posicaoBotaoComprar = criarMapasDePosicoes()

            testeOCR(posicoesLotes, posicaoCarteira)

        #Close Program
        elif opcao == '4':
            #TODO Sair do programa
            print('\tFechando programa...')
            go = False

        else:
            print('\tOpção inválida...')



        print('\n')





# INICIO <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
main()