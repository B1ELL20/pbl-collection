import random


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