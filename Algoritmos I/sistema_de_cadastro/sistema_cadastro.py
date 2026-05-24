# Código do problema 01 do PBL de Algoritmos: ponto de autoatendimento do restaurante universitário da UEFS 
# Código desenvolvido único e exclusivamente por Gabriel Dantas Costa Carneiro sem utilização de ferramentas de inteligência artificial
# Aluno: Gabriel Dantas Costa Carneiro // Matrícula: 26111296
# Professora: Michele Fúlvia Angelo

import json

# Variáveis e constantes globais de controle do sistema
system_on = True
ARQUIVO_JOGADORES = "jogadores.json"

def carregar_jogadores():
    lista_jogadores = []
    try:
        # Abre o arquivo para leitura
        with open("jogadores.json", "r", encoding="utf-8") as f:
            dados_do_arquivo = json.load(f)  # Carrega a lista de dicionários
            
            # Converte cada dicionário de volta para um objeto Player
            for dados in dados_do_arquivo:
                # 1. Cria o objeto apenas com o id e o nome (como o __init__ exige)
                jogador = Player(dados["id"], dados["name"])
                
                # 2. Restaura os outros atributos que estavam salvos
                jogador.victories = dados["victories"]
                jogador.defeats = dados["defeats"]
                jogador.draws = dados["draws"]
                jogador.score = dados["score"]
                
                # 3. Adiciona o objeto pronto na lista
                lista_jogadores.append(jogador)
                
    except FileNotFoundError:
        # Se o arquivo não existir (primeira execução), retorna a lista vazia
        return []
        
    return lista_jogadores

class Player:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.victories = 0
        self.defeats = 0
        self.draws = 0
        self.score = 0
    
    def for_dict(self):
        return self.__dict__

class Match:
    def __init__(self, player1_id, player2_id):
        self.player1 = player1_id
        self.player1 = player2_id


def show_menu():
    print("\n=== MENU DO CAMPEONATO ===")
    print("1 - Cadastrar um jogador")
    print("2 - Registrar uma partida")
    print("3 - Consultar um jogador")
    print("4 - Exibir Ranking do campeonato")
    print("5 - Gerar relatório do campeonato")
    print("6 - Sair")

while system_on:

    show_menu()
    option = input("\nEscolha uma opção: ")

    match option:

        case "1":
            new_players = []
            print("\n[Você escolheu: Cadastrar um jogador]")
            jogadores_registrados = carregar_jogadores()
            name = input("Digite o nome do jogador: ")

            if len(jogadores_registrados) > 0:

                for jogador in jogadores_registrados:

                    if jogador.name == name:
                        name = input('Nome já existe, digite um nome novamente!')

                id_max = 0

                for jogador in jogadores_registrados:

                    if jogador.id > id_max:
                        id_max = jogador.id

                jogador = Player(id_max + 1, name)

                new_players = [jogador.for_dict() for jogador in jogadores_registrados]
                new_players.append(jogador.for_dict())

            else:
                jogador = Player(1, name)
                new_players = [jogador.for_dict()]

            with open("jogadores.json", "w") as f:
                json.dump(new_players, f, indent=4)

        case "1":
            print("\n[Você escolheu: Cadastrar um jogador]")
        case "1":
            print("\n[Você escolheu: Cadastrar um jogador]")
        case "1":
            print("\n[Você escolheu: Cadastrar um jogador]")
        case "1":
            print("\n[Você escolheu: Cadastrar um jogador]")
        case "1":
            print("\n[Você escolheu: Cadastrar um jogador]")
        case _:
            print("\n[Você escolheu: Cadastrar um jogador]")