from collections import deque


import random
from collections import deque

def gerar_labirinto(tamanho):
    config = {11: 1, 15: 2, 19: 3}
    qtd = config.get(tamanho, 1)

    # 1. Criar base de paredes
    labirinto = [[2 for _ in range(tamanho)] for _ in range(tamanho)]

    # 2. Definir Início e Fim (Quinas opostas)
    p_x, p_y = random.choice([(0,0), (0, tamanho-1), (tamanho-1, 0), (tamanho-1, tamanho-1)])
    f_x, f_y = (tamanho-1) - p_x, (tamanho-1) - p_y

    # 3. Algoritmo de Escavação (DFS)
    def cavar(x, y):
        labirinto[y][x] = 3
        direcoes = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcoes)
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if 0 <= nx < tamanho and 0 <= ny < tamanho and labirinto[ny][nx] == 2:
                labirinto[y + dy // 2][x + dx // 2] = 3
                cavar(nx, ny)

    cavar(p_x, p_y)
    labirinto[p_y][p_x] = 1
    labirinto[f_y][f_x] = 4

    # 4. Colocar Porta (7) ao redor da chegada
    for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        ny, nx = f_y + dy, f_x + dx
        if 0 <= ny < tamanho and 0 <= nx < tamanho and labirinto[ny][nx] == 3:
            labirinto[ny][nx] = 7

    # 5. Mapear distâncias reais a partir do jogador (BFS)
    # Isso garante que sabemos quem está perto e quem está longe
    distancias = {}
    fila = deque([(p_x, p_y, 0)])
    visitados = {(p_x, p_y)}
    
    while fila:
        x, y, d = fila.popleft()
        if labirinto[y][x] == 3: # Só consideramos caminhos livres para itens
            distancias[(x, y)] = d
        
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < tamanho and 0 <= ny < tamanho and (nx, ny) not in visitados:
                if labirinto[ny][nx] in [3, 7]: # Caminho ou porta
                    visitados.add((nx, ny))
                    fila.append((nx, ny, d + 1))

    # Ordenar espaços livres pela distância do jogador
    espacos_ordenados = sorted(distancias.keys(), key=lambda p: distancias[p])
    
    # 6. Distribuir Itens com base na distância
    # Dividimos o caminho em 3 zonas: Perto (Espadas), Meio (Moedas/Chave), Longe (Monstros)
    terco = len(espacos_ordenados) // 3
    
    zona_perto = espacos_ordenados[:terco]
    zona_meio = espacos_ordenados[terco:terco*2]
    zona_longe = espacos_ordenados[terco*2:]

    # Colocar Espadas (Sempre na zona inicial)
    for _ in range(qtd):
        pos = zona_perto.pop(random.randrange(len(zona_perto)))
        labirinto[pos[1]][pos[0]] = 9

    # Colocar Monstros (Sempre na zona final/longe)
    for _ in range(qtd):
        pos = zona_longe.pop(random.randrange(len(zona_longe)))
        labirinto[pos[1]][pos[0]] = 8

    # Colocar Chave (No meio do caminho)
    pos_chave = zona_meio.pop(random.randrange(len(zona_meio)))
    labirinto[pos_chave[1]][pos_chave[0]] = 6

    # Colocar Moedas (Espalhadas no que sobrou)
    sobras = zona_perto + zona_meio + zona_longe
    for _ in range(qtd):
        pos = sobras.pop(random.randrange(len(sobras)))
        labirinto[pos[1]][pos[0]] = 5

    return labirinto