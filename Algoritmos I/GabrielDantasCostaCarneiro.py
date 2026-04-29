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

    subprocess.run('cls', shell=True)
    print(lateral)
    for i in labirinto:

        linha = '\u25A0 '

        for j in i:

            linha += str(j) + ' '

        print(linha
              .replace('2', '\u25A0')
              .replace('3', ' ')
              .replace('1', '\U0001FBC6')
              .replace('6', '\U0001F5DD')
              .replace('7', '\033[31m\u25A0\033[0m')
              .replace('4', '\033[31m\u25CF\033[0m') + '\u25A0')
    print(lateral)

def gerar_labirinto(tamanho):

    global personagem_x
    global personagem_y

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

    def cavar_caminho(x, y):

        if x != personagem_x or y != personagem_y:
            labirinto[y][x] = 3 
        
        direcoes = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcoes)
        
        for direcao_x, direcao_y in direcoes:
            passos_x = x + direcao_x
            passos_y = y + direcao_y
            
            if passos_x >= 0 and passos_x < tamanho and passos_y >= 0 and passos_y < tamanho and labirinto[passos_y][passos_x] == 'X':
                labirinto[y + direcao_y // 2][x + direcao_x // 2] = 3
                cavar_caminho(passos_x, passos_y)
    
    cavar_caminho(personagem_x, personagem_y)

    if y_final == tamanho - 1: 
        labirinto[y_final - 1][x_final] = 7

    elif x_final == tamanho - 1: 
        labirinto[y_final][x_final - 1] = 7

    labirinto[y_final][x_final] = 4

    chave_x = random.randint(0, tamanho - 1)
    chave_y = random.randint(0, tamanho - 1)

    while labirinto[chave_y][chave_x] != 3:
        chave_x = random.randint(0, tamanho - 1)
        chave_y = random.randint(0, tamanho - 1)
    
    labirinto[chave_y][chave_x] = 6

    for i in range(tamanho):
        for j in range(tamanho):

            if (labirinto[i][j] == 'X'):
                labirinto[i][j] = 2

    return labirinto


print('-----------------')
print('1 - 8X8')
print('2 - 10X10')
print('3 - 15X15')
print('-----------------')
valor = input('\nEscolha o tamanho do labirinto: ')

while valor not in ['1', '2', '3']:
    print('Escolha uma opção válida!')
    valor = input('Escolha o tamanho do labirinto: ')

if valor == '1':
    tamanho = 9

elif valor == '2':
    tamanho = 11

else:
    tamanho = 15

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