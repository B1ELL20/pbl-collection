import os
import random
import time
import threading
from pynput import keyboard # Requer: pip install pynput

# Variáveis globais de estado
personagem_x, personagem_y = 0, 0
tamanho = 0
chaves, vidas, espadas, moedas = 0, 1, 0, 0
tempo_segundos = 0
tempo_finalizado = False
labirinto = []

def cronometro():
    global tempo_segundos, tempo_finalizado
    while not tempo_finalizado:
        # O segredo: \033[s salva a posição do cursor, \033[H vai pro topo, \033[u volta
        minutos = tempo_segundos // 60
        segundos = tempo_segundos % 60
        status = f" TEMPO: {minutos:02d}:{segundos:02d} | VIDAS: {vidas} | MOEDAS: {moedas} | ESPADAS: {espadas} | CHAVES: {chaves}"
        
        # Escreve o tempo no topo sem interferir na leitura das teclas
        print(f"\033[s\033[H\033[32m{status}\033[0m\033[K\033[u", end="", flush=True)
        
        time.sleep(1)
        tempo_segundos += 1

def mostrar_labirinto():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Deixamos a primeira linha vazia para o cronômetro que escreve via ANSI
    print("\n") 
    
    lateral = '\u25A0 ' * (tamanho + 2)
    print(lateral)
    for i in labirinto:
        linha = '\u25A0 '
        for j in i:
            item = str(j)
            # Substituições com cores
            item = item.replace('2', '\u25A0')
            item = item.replace('3', ' ')
            item = item.replace('1', '\033[93m\U0001FBC6\033[0m') # Personagem
            item = item.replace('5', '\033[33m✦\033[0m')         # Moeda
            item = item.replace('6', '\033[34m\U0001F5DD\033[0m') # Chave
            item = item.replace('7', '\033[31m\u25A0\033[0m')    # Porta
            item = item.replace('8', '\033[35m🕷\033[0m')         # Monstro
            item = item.replace('9', '\033[36m⚔\033[0m')         # Espada
            item = item.replace('4', '\033[32m\u25CF\033[0m')    # Saída
            linha += item + ' '
        print(linha + '\u25A0')
    print(lateral)
    print("\nUse W, A, S, D para mover. 'ESC' para sair.")

def ao_pressionar(key):
    global personagem_x, personagem_y, tempo_finalizado, vidas, moedas, chaves, espadas

    try:
        k = key.char.lower()
    except:
        k = key.name

    if k == 'esc':
        tempo_finalizado = True
        return False # Para o listener

    dx, dy = 0, 0
    if k == 'w': dy = -1
    elif k == 's': dy = 1
    elif k == 'a': dx = -1
    elif k == 'd': dx = 1
    else: return

    novo_x, novo_y = personagem_x + dx, personagem_y + dy

    # Verificação de colisão e lógica de jogo
    if 0 <= novo_x < tamanho and 0 <= novo_y < tamanho:
        destino = labirinto[novo_y][novo_x]
        
        if destino == 2: return # Parede

        if destino == 4: # Vitória
            tempo_finalizado = True
            mostrar_labirinto()
            print("\nPARABÉNS! VOCÊ ESCAPOU!")
            return False

        elif destino == 5: moedas += 1
        elif destino == 6: chaves += 1
        elif destino == 9: espadas += 1
        elif destino == 8: # Combate
            if espadas > 0: espadas -= 1
            else:
                vidas -= 1
                if vidas <= 0:
                    tempo_finalizado = True
                    mostrar_labirinto()
                    print("\nGAME OVER! Os monstros te pegaram.")
                    return False
        
        elif destino == 7: # Porta
            if chaves > 0: chaves -= 1
            else: return # Bloqueado

        # Move o personagem
        labirinto[personagem_y][personagem_x] = 3
        personagem_x, personagem_y = novo_x, novo_y
        labirinto[personagem_y][personagem_x] = 1
        mostrar_labirinto()

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
    

    terco = len(espacos_para_itens) // 3

    zona_perto = espacos_para_itens[:terco]
    zona_meio = espacos_para_itens[terco:-terco]
    zona_longe = espacos_para_itens[-terco:]

    random.shuffle(zona_perto)
    random.shuffle(zona_meio)
    random.shuffle(zona_longe)


    # ZONA PERTO (Início da lista) -> ESPADAS (9)
    for i in range(quantidade):
        pos = zona_perto.pop(0) # Pega os primeiros elementos
        labirinto[pos[1]][pos[0]] = 9

    # ZONA LONGE (Final da lista) -> MONSTROS (8)
    for i in range(quantidade):
        pos = zona_longe.pop() # Pega os últimos elementos
        labirinto[pos[1]][pos[0]] = 8

    # CHAVE (6) - Sorteamos uma posição que sobrou no meio
    pos_chave = zona_meio.pop(len(zona_meio) // 2)
    labirinto[pos_chave[1]][pos_chave[0]] = 6

    # MOEDAS (5) - Sorteamos em qualquer lugar que sobrou

    sobras = zona_perto + zona_meio + zona_longe
    random.shuffle(sobras)
    for i in range(quantidade):
        pos = sobras.pop()
        labirinto[pos[1]][pos[0]] = 5

    for i in range(tamanho):
        for j in range(tamanho):

            if (labirinto[i][j] == 'X'):
                labirinto[i][j] = 2

    return labirinto

# --- BLOCO PRINCIPAL (Simplificado para o exemplo) ---

os.system('cls' if os.name == 'nt' else 'clear')
print("Escolha: 1(11x11), 2(15x15), 3(19x19)")
op = input("> ")
tamanho = 11 if op == '1' else 15 if op == '2' else 19

# Use sua função gerar_labirinto original aqui
# (Supondo que ela retorne o labirinto e defina personagem_x/y)
labirinto = gerar_labirinto(tamanho) 

# Inicia Cronômetro
t = threading.Thread(target=cronometro, daemon=True)
t.start()

mostrar_labirinto()

# Listener da pynput: ele roda em background
with keyboard.Listener(on_press=ao_pressionar) as listener:
    listener.join()