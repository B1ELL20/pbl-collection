import subprocess
import random

personagem_x = 0
personagem_y = 0
tamanho = 0

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

        print(linha.replace('2', '\u25A0').replace('3', ' ').replace('1', '\U0001FBC6').replace('4', '\033[31m\u25CF\033[0m') + '\u25A0')
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

    personagem_x = random.randint(0, tamanho - 1)
    personagem_y = random.randint(0, tamanho - 1)

    while (personagem_y != 0 and personagem_y != tamanho - 1) and (personagem_x != 0 and personagem_x != tamanho - 1):
        personagem_x = random.randint(0, 2)

    labirinto[personagem_y][personagem_x] = 1

    x_final = 0
    y_final = 0

    if personagem_x == 0:
        x_final = tamanho - 1
    elif personagem_x == tamanho - 1:
        x_final = 0

    if personagem_y == 0:
        y_final = tamanho - 1
    elif personagem_y == tamanho - 1:
        y_final = 0

    labirinto[y_final][x_final] = 4

    for i in range(tamanho):
        for j in range(tamanho):

            numero = random.randint(2, 3)

            if (labirinto[i][j] != 1 and labirinto[i][j] != 4):
                labirinto[i][j] = numero

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
    tamanho = 8

elif valor == '2':
    tamanho = 10

else:
    tamanho = 15

labirinto = gerar_labirinto(tamanho)
mostrar_labirinto(labirinto, tamanho)

comando = ''

while comando != 'f':

    comando = input("Digite o movimento do seu personagem(W, A, S, D): ")

    match comando.lower():

        case 'w':

            labirinto[personagem_y][personagem_x] = 3
            if (personagem_y > 0 and labirinto[personagem_y - 1][personagem_x] != 2):
                personagem_y -= 1

        case 'a':

            labirinto[personagem_y][personagem_x] = 3
            if (personagem_x > 0 and labirinto[personagem_y][personagem_x - 1] != 2):
                personagem_x -= 1
            
        case 's':

            labirinto[personagem_y][personagem_x] = 3
            if (personagem_y + 1 < len(labirinto) and labirinto[personagem_y + 1][personagem_x] != 2):
                personagem_y += 1

        case 'd':

            labirinto[personagem_y][personagem_x] = 3
            if (personagem_x < len(labirinto[personagem_y]) and labirinto[personagem_y][personagem_x + 1] != 2):
                personagem_x += 1

        case _:

            print('Movimento inválido!')
    
    if labirinto[personagem_y][personagem_x] == 4:
        comando = 'f'
        print('Parabéns, você chegou ao final do labirinto!!')

    labirinto[personagem_y][personagem_x] = 1
    mostrar_labirinto(labirinto, tamanho)