# Código do problema 02 do PBL de Algoritmos: fuga do labirinto
# Código desenvolvido único e exclusivamente por Gabriel Dantas Costa Carneiro sem utilização de ferramentas de inteligência artificial
# Aluno: Gabriel Dantas Costa Carneiro // Matrícula: 26111296
# Professora: Michele Fúlvia Angelo


# ADICIONAR ITEM DE PICARETA
# FAZER CÁLCULO DA PUNTUAÇÃO FINAL ATRAVÉS DE MOEDAS TEMPO

# Importação de bibliotecas

import subprocess
import random
import time
import threading
from pynput import keyboard

# Variáveis globais

personagem_x = 0
personagem_y = 0
tamanho = 0
chaves = 0
vidas = 1
espadas = 0
moedas = 0
tempo_finalizado = False
caminho_percorrido = []

# Função cronometro

def cronometro():

    global tempo_finalizado

    tempo_segundos = 180

    while not tempo_finalizado:

        minutos = tempo_segundos // 60
        segundos = tempo_segundos % 60

        status = f" TEMPO: {minutos:02d}:{segundos:02d} | VIDAS: {vidas} | MOEDAS: {moedas} | ESPADAS: {espadas} | CHAVES: {chaves}"
        
        print(f"\033[s\033[H\033[32m{status}\033[0m\033[K\033[u", end="", flush=True)

        time.sleep(1)
        tempo_segundos -= 1
        if tempo_segundos == 0:
            tempo_finalizado = True


def mostrar_labirinto(labirinto, tamanho):

    subprocess.run('cls', shell=True)
    print('\n')

    borda = ''
    for i in range(tamanho + 2):
        borda += '\u25A0 '

    print(borda)
    for i in labirinto:

        linha = '\u25A0 '

        for j in i:

            linha += str(j) + ' '

        print(linha
                .replace('1', '\U0001FBC6')
                .replace('2', '\u25A0')
                .replace('3', ' ')
                .replace('4', '\033[31m\u25CF\033[0m')
                .replace('5', '\033[33m✦\033[0m')
                .replace('6', '\033[33m\U0001F5DD\033[0m')
                .replace('7', '\033[31m\u25A0\033[0m')
                .replace('8', '\033[35m🕷\033[0m')
                .replace('9', '\033[34m⚔\033[0m') 
                .replace('*', '\033[34m\u25CF\033[0m')+ '\u25A0')
    print(borda)

def gerar_labirinto(tamanho):

    global personagem_x, personagem_y

    quantidades_por_tamanho = {15: 2, 19: 3, 23: 4}
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
    caminho_percorrido.append((personagem_y, personagem_x))

    x_final = abs(personagem_x - (tamanho - 1))
    y_final = abs(personagem_y - (tamanho - 1))

    caminho_lista = []

    def cavar_caminho(x, y):

        if x != personagem_x or y != personagem_y:
            labirinto[y][x] = 3 
            caminho_lista.append((x, y))
        
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


    for p in caminho_lista:
        x = p[0]
        y = p[1]

        if labirinto[y][x] == 3:
            espacos_para_itens.append(p)
    
    terco = len(espacos_para_itens) // 3

    zona_perto = espacos_para_itens[:terco]
    zona_meio = espacos_para_itens[terco:-terco]
    zona_restante = espacos_para_itens[terco:]
    #zona_longe = espacos_para_itens[-terco:]

    random.shuffle(zona_perto)
    random.shuffle(zona_restante)
    random.shuffle(zona_meio)

    espadas_colocadas = 0

    for i in range(quantidade):

        if espadas_colocadas == 0:
            pos = zona_perto.pop()
            espadas_colocadas += 1
        else:
            pos = zona_restante.pop()

        labirinto[pos[1]][pos[0]] = 9

    for i in range(quantidade):
        pos = zona_restante.pop()
        labirinto[pos[1]][pos[0]] = 8

    pos_chave = zona_meio.pop(len(zona_meio) // 2)
    labirinto[pos_chave[1]][pos_chave[0]] = 6

    sobras = zona_perto + zona_restante
    random.shuffle(sobras)
    for i in range(quantidade):
        pos = sobras.pop()
        labirinto[pos[1]][pos[0]] = 5

    for i in range(tamanho):
        for j in range(tamanho):

            if (labirinto[i][j] == 'X'):
                labirinto[i][j] = 2

    return labirinto

def input_key(key):

    global personagem_x, personagem_y, tempo_finalizado, vidas, moedas, chaves, espadas
    global caminho_percorrido

    if tempo_finalizado:
        return False

    comando = ''

    try:
        comando = key.char.lower()
    except:
        comando = key.name

    if comando == 'esc':
        tempo_finalizado = True
        return False
    
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

            return
    
    
    if (passo_novo_x >= 0 and passo_novo_x < len(labirinto) and passo_novo_y >= 0 and passo_novo_y < len(labirinto) and  labirinto[passo_novo_y][passo_novo_x] != 2):

        labirinto[personagem_y][personagem_x] = 3

        
        if labirinto[passo_novo_y][passo_novo_x] == 4:
            print('Parabéns, você chegou ao final do labirinto!!')
            return False

        if labirinto[passo_novo_y][passo_novo_x] == 6:
            chaves += 1
        
        if labirinto[passo_novo_y][passo_novo_x] == 5:
            moedas += 1

        if labirinto[passo_novo_y][passo_novo_x] == 9:
            espadas += 1
        
        if labirinto[passo_novo_y][passo_novo_x] == 8 and espadas > 0:
            espadas -= 1

        elif labirinto[passo_novo_y][passo_novo_x] == 8 and espadas == 0:
            vidas -= 1

            if vidas == 0:
                return False

        if labirinto[passo_novo_y][passo_novo_x] == 7 and chaves > 0:
            chaves -= 1

        elif labirinto[passo_novo_y][passo_novo_x] == 7 and chaves == 0:
            passo_novo_x = personagem_x
            passo_novo_y = personagem_y

        labirinto[passo_novo_y][passo_novo_x] = 1

        personagem_x = passo_novo_x
        personagem_y = passo_novo_y

        caminho_percorrido.append((personagem_y, personagem_x))

    mostrar_labirinto(labirinto, tamanho)

print('BEM VINDO(A) AO LABIRINTO!')
print('AQUI ESTÃO AS REGRAS PARA EMBARCAR NESSA AVENTURA:')
print('-> ANDE PELO LABIRINTO COM AS TECLAS W(CIMA), A(ESQUERDA), S(BAIXO), D(DIREITA)')
print('-> SEU OBJETIVO É SUPERAR OS MONSTROS \033[35m🕷\033[0m , ENCONTRAR A CHAVE \033[33m\U0001F5DD\033[0m  E DESTRANCAR A PORTA FINAL \033[31m\u25A0\033[0m')
print('-> SE CONSEGUIR A ESFERA VERMELHA \033[31m\u25CF\033[0m, VOCÊ CONSEGUE A LIBERDADE DO LABIRINTO')
print('-> MAS CUIDADO! SE OS MONSTROS TE ENCONTRAREM SEM ESPADAS \033[34m⚔\033[0m , PODE SER RUIM PRA VOCÊ!')
print('-> NO LABIRINTO EXISTEM MOEDAS \033[33m✦\033[0m QUE CONTAM NA SUA PONTUAÇÃO, ASSIM COMO ESPADAS PARA SE DEFENDER')
print('-> EXISTE UM ITEM ESPECIAL DE PICARETA, QUE LHE PERMITE QUEBRAR QUALQUER PAREDE UMA ÚNICA VEZ')
print('-> POR FIM, CUIDADO COM O TEMPO, SEJA ÁGIL E SAIA O QUANTO ANTES!')
print('AGORA CHEGA DE CONVERSA! ESCOLHA O TAMANHO DO MAPA QUE DESEJA ENCARAR!')

print('--------------------------------------------------------------------------------------------------------------------------')
print('[1] - 15X15 -> UM MAPA PARA AMADORES')
print('[2] - 19X19 -> AQUI AS COISA JÁ NÃO SÃO TÃO SIMPLES')
print('[3] - 23X23 -> SE ESCOLHER É PORQUE SE GARANTE')
print('--------------------------------------------------------------------------------------------------------------------------')
valor = input('\nEscolha o tamanho do labirinto(1, 2 ou 3): ')

while valor not in ['1', '2', '3']:
    print('Escolha uma opção válida!')
    valor = input('Escolha o tamanho do labirinto: ')

if valor == '1':
    tamanho = 15

elif valor == '2':
    tamanho = 19

else:
    tamanho = 23

labirinto = gerar_labirinto(tamanho)

t = threading.Thread(target=cronometro, daemon=True)
t.start()

mostrar_labirinto(labirinto, tamanho)

with keyboard.Listener(on_press=input_key) as listener:
    listener.join()

for y, x in caminho_percorrido:

    labirinto[y][x] = '*'
    mostrar_labirinto(labirinto, tamanho)

if vidas == 0:
    print('OS MONSTROS TE PEGARAM, MAIS SORTE DA PRÓXIMA VEZ!')

elif tempo_finalizado: 
    print('TEMPO ESGOTADO! NÃO FOI DESSA VEZ!')

else:
    print('VOCÊ CONSEGUIU FUGIR DO LABIRINTO! PARABÉNS!!!')