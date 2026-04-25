import random

def gerar_labirinto(largura, altura):
    # Inicializa a matriz cheia de paredes (1 = parede, 0 = caminho)
    labirinto = [[1 for _ in range(largura)] for _ in range(altura)]
    
    def carvar_caminho(x, y):
        labirinto[y][x] = 0  # Marca a célula atual como caminho
        
        # Direções: (dx, dy) pulando 2 casas para manter as paredes entre os caminhos
        direcoes = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcoes)
        
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            
            # Verifica se a nova posição está dentro do mapa e se ainda é parede
            if 0 <= nx < largura and 0 <= ny < altura and labirinto[ny][nx] == 1:
                # Remove a parede entre a célula atual e a próxima
                labirinto[y + dy // 2][x + dx // 2] = 0
                carvar_caminho(nx, ny)

    # Começa o backtracking do canto superior esquerdo
    carvar_caminho(0, 0)
    return labirinto

# Exemplo de uso (use números ímpares para melhores resultados)
mapa = gerar_labirinto(21, 11)
for linha in mapa:
    print("".join("  " if celula == 0 else "██" for celula in linha))