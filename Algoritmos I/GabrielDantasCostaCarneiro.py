# Código do problema 02 do PBL de Algoritmos: fuga do labirinto
# Código desenvolvido único e exclusivamente por Gabriel Dantas Costa Carneiro sem utilização indevida de ferramentas de inteligência artificial
# Aluno: Gabriel Dantas Costa Carneiro // Matrícula: 26111296
# Professora: Michele Fúlvia Angelo

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
quantidade = 0
chaves = 0
vidas = 1
espadas = 0
moedas = 0
picaretas = 0
jogo_finalizado = False
tempo = 0
tempo_segundos = 0
caminho_percorrido = []

# Função cronometro para contagem regressiva e visualização de status

def cronometro():

    global jogo_finalizado, tempo_segundos

    while not jogo_finalizado:

        minutos = tempo_segundos // 60
        segundos = tempo_segundos % 60

        status = f" \033[32mTEMPO: {minutos:02d}:{segundos:02d}\033[0m | \033[31mVIDAS: {vidas}\033[0m | \033[33mMOEDAS: {moedas}\033[0m | \033[34mESPADAS: {espadas}\033[0m | \033[33mCHAVES: {chaves}\033[0m"
        
        print(f"\033[s\033[H{status}\033[K\033[u", end="", flush=True)

        time.sleep(1)
        tempo_segundos -= 1
        if tempo_segundos == 0:
            jogo_finalizado = True

# Função para visualização do labirinto

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
                .replace('P', '\033[32m⛏\033[0m') 
                .replace('C', '\033[31m❦\033[0m') 
                .replace('*', '\033[34m*\033[0m') + '\u25A0')
    print(borda)

# Declaração da função recursiva para "cavar" e registrar os caminhos do labirinto gerados aleatoriamente

def cavar_caminho(x, y, inicial_x, inicial_y, tamanho_matriz, caminho_lista, matriz_labirinto):

        if x != inicial_x or y != inicial_y:
            matriz_labirinto[y][x] = 3 
            caminho_lista.append((y, x))
        
        direcoes = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcoes)
        
        for direcao_x, direcao_y in direcoes:
            passos_x = x + direcao_x
            passos_y = y + direcao_y
            
            if passos_x >= 0 and passos_x < tamanho_matriz and passos_y >= 0 and passos_y < tamanho_matriz and matriz_labirinto[passos_y][passos_x] == 'X':
                matriz_labirinto[y + direcao_y // 2][x + direcao_x // 2] = 3
                caminho_lista.append((y + direcao_y // 2, x + direcao_x // 2))
                cavar_caminho(passos_x, passos_y, inicial_x, inicial_y, tamanho_matriz, caminho_lista, matriz_labirinto)

# Função para geração do labirinto

def gerar_labirinto(tamanho):

    global personagem_x, personagem_y, quantidade

    quantidades_por_tamanho = {15: 2, 19: 3, 23: 4}
    quantidade = quantidades_por_tamanho.get(tamanho, 1)

    # Matriz inicial gerada contendo apenas X

    labirinto = []
    for i in range(tamanho):
        linha = []
        for j in range(tamanho):

            linha.append("X")

        labirinto.append(linha)

    # Definição da posição inicial do personagem

    personagem_x = random.choice([0, tamanho - 1])
    personagem_y = random.choice([0, tamanho - 1])

    labirinto[personagem_y][personagem_x] = 1
    caminho_percorrido.append((personagem_y, personagem_x))

    # Definição da posição da saída

    x_final = abs(personagem_x - (tamanho - 1))
    y_final = abs(personagem_y - (tamanho - 1))

    caminho = []
    
    # Execução inicial da função cavar_caminho recebendo como parâmetro as posições iniciais do jogador
    cavar_caminho(personagem_x, personagem_y, personagem_x, personagem_y, tamanho, caminho, labirinto)

    # Atribuit o valor da saída nas coordenadas da saída
    labirinto[y_final][x_final] = 4

    # Atribuir portas ao redos da saída, conforme posição

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
    

    # Criação de zonas para distribuição aleatória de itens

    espacos_para_itens = []

    for p in caminho:

        if labirinto[p[0]][p[1]] == 3:
            espacos_para_itens.append(p)
    
    terco = len(espacos_para_itens) // 3

    zona_perto = espacos_para_itens[:terco]
    zona_meio = espacos_para_itens[terco:-terco]
    zona_restante = espacos_para_itens[terco:]

    random.shuffle(zona_perto)
    random.shuffle(zona_restante)
    random.shuffle(zona_meio)

    # Distribuição de itens em cada zona aplicada logicamente

    # Distribuição de espadas

    espadas_colocadas = 0

    for i in range(quantidade):

        if espadas_colocadas == 0:
            pos_espada = zona_perto.pop()
            espadas_colocadas += 1
            labirinto[pos_espada[0]][pos_espada[1]] = 9
            
        else:
            pos_espada = zona_restante.pop()
            labirinto[pos_espada[0]][pos_espada[1]] = 9

    # Distribuição de monstros

    for i in range(quantidade):
        pos_monstro = zona_restante.pop()
        labirinto[pos_monstro[0]][pos_monstro[1]] = 8
    
    # Distribuição da chave

    pos_chave = zona_meio.pop()
    labirinto[pos_chave[0]][pos_chave[1]] = 6

    # Distribuição da picareta

    pos_picareta = zona_perto.pop()
    labirinto[pos_picareta[0]][pos_picareta[1]] = 'P'

    # Distribuição das moedas

    random.shuffle(zona_restante)
    for i in range(quantidade):
        pos_moedas= zona_restante.pop()
        labirinto[pos_moedas[0]][pos_moedas[1]] = 5
    
    # Distribuição da comida

    pos_comida = zona_restante.pop()
    labirinto[pos_comida[0]][pos_comida[1]] = 'C'

    # Substituição dos valores X que sobram pelo valor da parede

    for i in range(tamanho):
        for j in range(tamanho):

            if (labirinto[i][j] == 'X'):
                labirinto[i][j] = 2

    return labirinto

# Função para leitura das entradas via teclado

def entrada_de_comando(key):

    global personagem_x, personagem_y, jogo_finalizado, vidas, moedas, chaves, espadas, picaretas, caminho_percorrido

    if jogo_finalizado:
        return False

    comando = ''

    # Tenta receber o comando, caso contrário, recebe o nome do comando pressionado

    try:
        comando = key.char.lower()
    except:
        comando = key.name

    # Caso esc, finaliza o jogo

    if comando == 'esc':
        jogo_finalizado = True
        return False
    
    passo_novo_x = personagem_x
    passo_novo_y = personagem_y

    # Caso algum comando válido, anda para a posição correspondente

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
    
    
    # Valida a possibilidade do comando digitado e caso possível, realiza interação com o elemento encontrado

    if (passo_novo_x >= 0 and passo_novo_x < len(labirinto) 
        and passo_novo_y >= 0 and passo_novo_y < len(labirinto) 
        and ((labirinto[passo_novo_y][passo_novo_x] != 2) or picaretas > 0)):

        labirinto[personagem_y][personagem_x] = 3
        
        if labirinto[passo_novo_y][passo_novo_x] == 4:
            return False

        if labirinto[passo_novo_y][passo_novo_x] == 6:
            chaves += 1
        
        if labirinto[passo_novo_y][passo_novo_x] == 'C':
            vidas += 1
        
        if labirinto[passo_novo_y][passo_novo_x] == 5:
            moedas += 1

        if labirinto[passo_novo_y][passo_novo_x] == 9:
            espadas += 1
        
        if labirinto[passo_novo_y][passo_novo_x] == 'P':
            picaretas += 1

        if labirinto[passo_novo_y][passo_novo_x] == 2 and picaretas > 0:
            picaretas -= 1
        
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

    # Mostra o labirinto atualizado

    mostrar_labirinto(labirinto, tamanho)

# Apresentação das regras do jogo

print('BEM VINDO(A) AO LABIRINTO!')
print('AQUI ESTÃO AS REGRAS PARA EMBARCAR NESSA AVENTURA:')
print('-> ANDE PELO LABIRINTO COM AS TECLAS W(CIMA), A(ESQUERDA), S(BAIXO), D(DIREITA)')
print('-> SEU OBJETIVO É SUPERAR OS MONSTROS \033[35m🕷\033[0m , ENCONTRAR A CHAVE \033[33m\U0001F5DD\033[0m  E DESTRANCAR A PORTA FINAL \033[31m\u25A0\033[0m')
print('-> SE CONSEGUIR A ESFERA VERMELHA \033[31m\u25CF\033[0m, VOCÊ CONSEGUE A LIBERDADE DO LABIRINTO')
print('-> MAS CUIDADO! SE OS MONSTROS TE ENCONTRAREM SEM ESPADAS \033[34m⚔\033[0m , PODE SER RUIM PRA VOCÊ')
print('-> NO LABIRINTO O TEMPO E A MOEDAS \033[33m✦\033[0m CONTAM NA SUA PONTUAÇÃO')
print('-> EXISTE UM ITEM ESPECIAL DE PICARETA \033[32m⛏\033[0m , QUE LHE PERMITE QUEBRAR QUALQUER PAREDE UMA ÚNICA VEZ')
print('-> EXISTE UM ITEM ESPECIAL FRUTA CORAÇÃO \033[31m❦\033[0m, QUE LHE DÁ UMA VIDA EXTRA')
print('-> POR FIM, CUIDADO COM O TEMPO, SEJA ÁGIL E SAIA O QUANTO ANTES!')
print('AGORA CHEGA DE CONVERSA! ESCOLHA O TAMANHO DO MAPA QUE DESEJA ENCARAR!')

# Apresentação do menu para escolha do tamanho do labirinto

print('--------------------------------------------------------------------------------------------------------------------------')
print('[1] - 15X15 -> UM MAPA PARA AMADORES')
print('[2] - 19X19 -> AQUI AS COISA JÁ NÃO SÃO TÃO SIMPLES')
print('[3] - 23X23 -> SE ESCOLHER É PORQUE SE GARANTE')
print('--------------------------------------------------------------------------------------------------------------------------')

valor = input('\nEscolha o tamanho do labirinto(1, 2 ou 3): ')

while valor not in ['1', '2', '3']:
    print('Escolha uma opção válida!')
    valor = input('Escolha o tamanho do labirinto: ')

# Valores atribuídos conforme valor escolhido

if valor == '1':
    tamanho = 15
    tempo = 60
    tempo_segundos = 60

elif valor == '2':
    tamanho = 19
    tempo = 90
    tempo_segundos = 90

else:
    tamanho = 23
    tempo = 120
    tempo_segundos = 120

# Geração da matriz do labirinto atribuindo em uma variável

labirinto = gerar_labirinto(tamanho)

# Aplicação do cronômetro em uma thread

t = threading.Thread(target=cronometro, daemon=True)
t.start()

# Primeira visualização do labirinto

mostrar_labirinto(labirinto, tamanho)

# Listener para ouvir comandos vindos do teclado enquanto labirinto já foi executado

with keyboard.Listener(on_press=entrada_de_comando) as listener:
    listener.join()

# Visualização do caminho percorrido pelo jogador

for y, x in caminho_percorrido:

    labirinto[y][x] = '*'
    mostrar_labirinto(labirinto, tamanho)

# Mensagens conforme condição de parada do sistema

if jogo_finalizado and tempo_segundos > 0:
    print('Vai fugir? Até mais, volte sempre! >:)')

else:
    if vidas == 0:
        print('OS MONSTROS TE PEGARAM, MAIS SORTE DA PRÓXIMA VEZ!')

    elif tempo_segundos <= 0: 
        print('TEMPO ESGOTADO! NÃO FOI DESSA VEZ!')

    else:
        desempenho = 0

        if tempo_segundos >= tempo / 2:
            desempenho = (100 + ((moedas / quantidade) * 100)) / 2

        else: 
            desempenho = (((tempo_segundos / (tempo / 2)) * 100) + ((moedas / quantidade) * 100)) / 2
        
        minutos = tempo_segundos // 60
        segundos = tempo_segundos % 60

        print(f"Você concluiu o labirinto com desempenho de {desempenho:.0f}%")
        print(f'Pegou {moedas}/{quantidade} moedas e concluiu faltando {minutos:02d}:{segundos:02d} para acabar!')
        print('VOCÊ CONSEGUIU FUGIR DO LABIRINTO! PARABÉNS!!!')
