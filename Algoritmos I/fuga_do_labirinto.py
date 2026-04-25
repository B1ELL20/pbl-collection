import subprocess
import random

personagem_x = 0
personagem_y = 0
tamanho = 0

# Fazer chave ser gerada em um dos quadrantes opostos ao personagem e ao fim.
# Fazer final ser coberto por paredes e uma porta
# Fazer contador de tempo

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
            labirinto[y][x] = 3  # Marca a célula atual como caminho
        
        # Direções: (dx, dy) pulando 2 casas para manter as paredes entre os caminhos
        direcoes = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcoes)
        
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            
            # Verifica se a nova posição está dentro do mapa e se ainda é parede
            if 0 <= nx < tamanho and 0 <= ny < tamanho and labirinto[ny][nx] == 'X':
                # Remove a parede entre a célula atual e a próxima
                labirinto[y + dy // 2][x + dx // 2] = 3
                cavar_caminho(nx, ny)
    
    cavar_caminho(personagem_x, personagem_y)

    
    # Se o destino for cercado por paredes, "quebramos" uma parede vizinha
    # para garantir que ele esteja conectado ao resto do labirinto
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