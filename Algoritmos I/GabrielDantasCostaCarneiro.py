# Código do problema 02 do PBL de Algoritmos: fuga do labirinto
# Código desenvolvido único e exclusivamente por Gabriel Dantas Costa Carneiro sem utilização de ferramentas de inteligência artificial
# Aluno: Gabriel Dantas Costa Carneiro // Matrícula: 26111296
# Professora: Michele Fúlvia Angelo

import subprocess
import random
import time

personagem_x = 0
personagem_y = 0
tamanho = 0
chaves = 0
tempo_restante = 180

def mostrar_labirinto(labirinto, tamanho):


    lateral = ''
    for i in range(tamanho + 2):
        lateral += '\u25A0 '

    #subprocess.run('cls', shell=True)
    print(lateral)
    for i in labirinto:

        linha = '\u25A0 '

        for j in i:

            linha += str(j) + ' '

        print(linha
              .replace('2', '\u25A0')
              .replace('3', ' ')
              .replace('1', '\U0001FBC6')
              .replace('5', '✦')
              .replace('6', '\U0001F5DD')
              .replace('7', '\033[31m\u25A0\033[0m')
              .replace('8', '🕷')
              .replace('9', '⚔')
              .replace('4', '\033[31m\u25CF\033[0m') + '\u25A0')
    print(lateral)

def gerar_labirinto(tamanho):

    global personagem_x
    global personagem_y

    quantidades_por_tamanho = {11: 1, 15: 2, 19: 3}
    quantidade = quantidades_por_tamanho.get(tamanho, 1)

    labirinto = []
    for i in range(tamanho):
        linha = []
        for j in range(tamanho):

            linha.append("X")

        labirinto.append(linha)

    personagem_x = random.choice([0, tamanho - 1])
    personagem_y = random.choice([0, tamanho - 1])

    labirinto[personagem_y][personagem_x] = 1

    x_final = abs(personagem_x - (tamanho - 1))
    y_final = abs(personagem_y - (tamanho - 1))

    caminho_lista = [] # Vai guardar a ordem das células cavadas

    def cavar_caminho(x, y):

        if x != personagem_x or y != personagem_y:
            labirinto[y][x] = 3 
            caminho_lista.append((x, y)) # Salva a posição
        
        direcoes = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcoes)
        
        for direcao_x, direcao_y in direcoes:
            passos_x = x + direcao_x
            passos_y = y + direcao_y
            
            if passos_x >= 0 and passos_x < tamanho and passos_y >= 0 and passos_y < tamanho and labirinto[passos_y][passos_x] == 'X':
                labirinto[y + direcao_y // 2][x + direcao_x // 2] = 3
                caminho_lista.append((x + direcao_x // 2, y + direcao_y // 2))
                cavar_caminho(passos_x, passos_y)
    
    cavar_caminho(personagem_x, personagem_y)
    labirinto[y_final][x_final] = 4

    if y_final == 0:
         
         if labirinto[y_final + 1][x_final] == 3:
              labirinto[y_final + 1][x_final] = 7
    else:
              
         if labirinto[y_final - 1][x_final] == 3:
              labirinto[y_final - 1][x_final] = 7
    
    if x_final == 0:
         
         if labirinto[y_final][x_final + 1] == 3:
              labirinto[y_final][x_final + 1] = 7
    else:
              
         if labirinto[y_final][x_final - 1] == 3:
              labirinto[y_final][x_final - 1] = 7
    
    espacos_para_itens = []
    
    # Percorremos cada coordenada que foi cavada anteriormente
    for p in caminho_lista:
        x = p[0]
        y = p[1]
        
        # Verificamos se aquele lugar ainda é um caminho livre (3)
        # Isso evita colocar itens em cima do personagem (1), da chegada (4) ou porta (7)
        if labirinto[y][x] == 3:
            espacos_para_itens.append(p)


    # ZONA PERTO (Início da lista) -> ESPADAS (9)
    for i in range(quantidade):
        pos = espacos_para_itens.pop(0) # Pega os primeiros elementos
        labirinto[pos[1]][pos[0]] = 9

    # ZONA LONGE (Final da lista) -> MONSTROS (8)
    for i in range(quantidade):
        pos = espacos_para_itens.pop() # Pega os últimos elementos
        labirinto[pos[1]][pos[0]] = 8

    # CHAVE (6) - Sorteamos uma posição que sobrou no meio
    pos_chave = espacos_para_itens.pop(len(espacos_para_itens) // 2)
    labirinto[pos_chave[1]][pos_chave[0]] = 6

    # MOEDAS (5) - Sorteamos em qualquer lugar que sobrou
    random.shuffle(espacos_para_itens)
    for i in range(quantidade):
        pos = espacos_para_itens.pop()
        labirinto[pos[1]][pos[0]] = 5

    for i in range(tamanho):
        for j in range(tamanho):

            if (labirinto[i][j] == 'X'):
                labirinto[i][j] = 2

    return labirinto


print('-----------------')
print('1 - 11X11')
print('2 - 15X15')
print('3 - 19X19')
print('-----------------')
valor = input('\nEscolha o tamanho do labirinto: ')

while valor not in ['1', '2', '3']:
    print('Escolha uma opção válida!')
    valor = input('Escolha o tamanho do labirinto: ')

if valor == '1':
    tamanho = 11

elif valor == '2':
    tamanho = 15

else:
    tamanho = 19

labirinto = gerar_labirinto(tamanho)
mostrar_labirinto(labirinto, tamanho)

comando = ''

while comando != 'f':

    comando = input("Digite o movimento do seu personagem(W, A, S, D): ")

    passo_novo_x = personagem_x
    passo_novo_y = personagem_y

    match comando.lower():

        case 'w':
                passo_novo_y -= 1

        case 'a':
                passo_novo_x -= 1
            
        case 's':
                passo_novo_y += 1

        case 'd':
                passo_novo_x += 1

        case _:

            print('Movimento inválido!')

    if (passo_novo_x >= 0 and passo_novo_x < len(labirinto[passo_novo_y]) and passo_novo_y >= 0 and passo_novo_y < len(labirinto) and  labirinto[passo_novo_y][passo_novo_x] != 2):

        labirinto[personagem_y][personagem_x] = 3

        
        if labirinto[passo_novo_y][passo_novo_x] == 4:
            comando = 'f'
            print('Parabéns, você chegou ao final do labirinto!!')

        if labirinto[passo_novo_y][passo_novo_x] == 6:
            chaves += 1

        if labirinto[passo_novo_y][passo_novo_x] == 7 and chaves > 0:
            chaves -= 1

        elif labirinto[passo_novo_y][passo_novo_x] == 7 and chaves == 0:
            passo_novo_x = personagem_x
            passo_novo_y = personagem_y

        labirinto[passo_novo_y][passo_novo_x] = 1

        personagem_x = passo_novo_x
        personagem_y = passo_novo_y
        
    mostrar_labirinto(labirinto, tamanho)