# Código do problema 03 do PBL de Algoritmos: sistema Maze Masters 
# Código desenvolvido único e exclusivamente por Gabriel Dantas Costa Carneiro sem utilização indevida de ferramentas de inteligência artificial
# Aluno: Gabriel Dantas Costa Carneiro // Matrícula: 26111296
# Professora: Michele Fúlvia Angelo

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Variáveis e constantes globais de controle do sistema
system_on = True
PLAYERS_ARCHIVE = BASE_DIR / "jogadores.json"
MATCHS_ARCHIVE = BASE_DIR / "partidas.json"
REPORT_ARCHIVE = BASE_DIR / "relatorio.txt"

def input_validation_string(min_len):

    try:
        min_len = int(min_len)
        if min_len < 0:
            return print('O parâmetro de tamanho mínimo da string deve ser um inteiro positivo ou igual a zero!')

    except:
        return print('O parâmetro de tamanho mínimo da string deve ser um inteiro!')


    value = input()

    while len(value) < min_len:
        print(f'Valor inválido, número de caracteres mínimo deve ser {min_len}! Digite o valor corretamente.')
        value = input()

    return value

def input_validation_int():

    value = input()
    while not isinstance(value, int):

        try:
            value = int(value)
            assert value >= 0

        except:
            print('O valor deve ser um inteiro positivo ou igual a zero!')
            print('Digite o valor novamente:')
            value = input()

    return value


def fetch_players():

    lista_jogadores = []

    try:
        with open(PLAYERS_ARCHIVE, "r", encoding="utf-8") as f:
            dados_do_arquivo = json.load(f)
            
            for dados in dados_do_arquivo:
                jogador = Player(dados["id"], dados["name"])

                jogador.victories = dados["victories"]
                jogador.defeats = dados["defeats"]
                jogador.draws = dados["draws"]
                jogador.score = dados["score"]
                jogador.sequential_victories = dados["sequential_victories"]
                jogador.max_sequential_victories = dados["max_sequential_victories"]

                for h in dados["history"]:
                    history = History(h["match_id"], h["oponent_id"], h["oponent_name"], h["result"])
                    jogador.history.append(history)
                
                lista_jogadores.append(jogador)
                
    except FileNotFoundError:
        return []
        
    return lista_jogadores


def fetch_matchs():

    matchs_list = []

    try:

        with open(MATCHS_ARCHIVE, "r", encoding="utf-8") as f:
            dados_do_arquivo = json.load(f)  
            
            for dados in dados_do_arquivo:

                match = Match(
                    dados["id"],
                    dados["player1_id"],
                    dados["player2_id"],
                    dados["draw"],
                    dados["winner_id"])

                matchs_list.append(match)
                
    except FileNotFoundError:

        return []
        
    return matchs_list

def register_player(name):

    new_players = []
    jogadores_registrados = fetch_players()

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

    try:
        with open(PLAYERS_ARCHIVE, "w") as f:
            json.dump(new_players, f, indent=4)
        
        print('\nJogador cadastrado com sucesso!')

    except:
        return print('Erro ao cadastrar jogador!')
    

def register_match(player1_id, player2_id):

    new_matchs = []
    new_players = []
    winner_id = 0
    result_player_1 = ''
    result_player_2 = ''
    players = fetch_players()
    register_matchs = fetch_matchs()

    player1 = False
    player2 = False

    for player in players:

        if player.id == int(player1_id):
            player1 = player
        
        if player.id == int(player2_id):
            player2 = player

    if player1 != False and player2 != False:

        draw = input('Houve empate? (s/n)')

        while draw.lower() not in ['s', 'n']:
            print('Digite apenas o s para SIM e n para Não!')
            draw = input('Houve empate? (s/n)')

        if draw.lower() == 's':
            draw = True
            player1.draws += 1
            player1.score += 1
            player2.draws += 1
            player2.score += 1
            result_player_1 = 'Empatou'
            result_player_2 = 'Empatou'

        else:
            draw = False
            print(f'Jogador 1: {player1.name} | Jogador 2: {player2.name}')
            winner = input('Qual jogador que venceu? (1/2)')

            if winner == '1':
                winner_id = player1_id
                player1.victories += 1
                player1.score += 3
                player2.defeats += 1
                player2.score -= 1 if player2.score > 0 else 0
                result_player_1 = 'Ganhou'
                result_player_2 = 'Perdeu'

                if len(player1.history) > 0:
                    if player1.history[-1].result == 'Ganhou':
                        player1.sequential_victories += 1
                    else:
                        player1.sequential_victories = 1
                    
                    if player1.sequential_victories > player1.max_sequential_victories:
                        player1.max_sequential_victories = player1.sequential_victories
                else:
                    player1.sequential_victories = 1
                    player1.max_sequential_victories = 1

            else:
                winner_id = player2_id                           
                player2.victories += 1
                player2.score += 3
                player1.defeats += 1
                player1.score -= 1 if player1.score > 0 else 0 
                result_player_1 = 'Perdeu'
                result_player_2 = 'Ganhou'

                if len(player2.history) > 0:
                    if player2.history[-1].result == 'Ganhou':
                        player2.sequential_victories += 1
                    else:
                        player2.sequential_victories = 1
                    
                    if player2.sequential_victories > player2.max_sequential_victories:
                        player2.max_sequential_victories = player2.sequential_victories
                else:
                    player2.sequential_victories = 1
                    player2.max_sequential_victories = 1

        
        id_max = 0
        if len(register_matchs) > 0:
            for match in register_matchs:
                if match.id > id_max:
                    id_max = match.id

        new_match = Match(id_max + 1, player1_id, player2_id, draw, winner_id)
        new_matchs = [match.for_dict() for match in register_matchs]
        new_matchs.append(new_match.for_dict())

        history_player1 = History(new_match.id, player2_id, player2.name, result_player_1)
        history_player2 = History(new_match.id, player1_id, player1.name, result_player_2)

        player1.history.append(history_player1)
        player2.history.append(history_player2)

        for player in players:

            if player.id != int(player1_id) and player.id != int(player2_id):
                new_players.append(player.for_dict())
        
        new_players.append(player1.for_dict())
        new_players.append(player2.for_dict())

        with open(MATCHS_ARCHIVE, "w") as f:
            json.dump(new_matchs, f, indent=4)

        with open(PLAYERS_ARCHIVE, "w") as f:
            json.dump(new_players, f, indent=4)
    else:
        print('Ids especificados não existem!')

def get_player(id):

    players = fetch_players()
    exists_player = False
    for player in players:
        if player.id == int(id):

            exists_player = True
            print(f'Id: {player.id}')
            print(f'Nome: {player.name}')
            print(f'Vitórias: {player.victories}')
            print(f'Derrotas: {player.defeats}')
            print(f'Empates: {player.draws}')
            print(f'Pontuação: {player.score}')

            print('Histórico de partidas disputadas:')

            if len(player.history) > 0:

                print("\n" + "=" * 32)
                print(f"{'Adversário':<20} {'Resultado':<10}")
                print("=" * 32)

                for h in player.history:
                    print(f"{h.oponent_name:<20} {h.result:<10}")
                print("=" * 32)
            else:
                print("Sem partidas disputadas por esse jogador!")

    if not exists_player:
        print('O jogador especificado não existe!')

def ranking_players(players):

    tamanho = len(players)
    for i in range(0, tamanho-1):
        min = i
        for j in range(i+1, tamanho):

            if players[j].score > players[min].score:
                min = j
            elif players[j].score == players[min].score and players[j].victories > players[min].victories:
                min = j
            elif players[j].score == players[min].score and players[j].victories == players[min].victories and players[j].draws > players[min].draws:
                min = j
            elif players[j].score == players[min].score and players[j].victories == players[min].victories and players[j].draws == players[min].draws and players[j].defeats < players[min].defeats:
                min = j

        players[i], players[min] = players[min], players[i]

    return players

def get_player_more_defeats():

    players = fetch_players()
    player_id = 0
    more_defeats = 0

    for player in players:

        if player.defeats > more_defeats:
            more_defeats = player.defeats
            player_id = player.id

    for player in players:

        if player_id == player.id:
            return player
        
def get_player_more_sequential_victories():

    players = fetch_players()
    player_id = 0
    more_sequential_victories = 0

    for player in players:

        if player.max_sequential_victories > more_sequential_victories:
            more_sequential_victories = player.max_sequential_victories
            player_id = player.id

    for player in players:

        if player_id == player.id:
            return player

class Player:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.victories = 0
        self.defeats = 0
        self.draws = 0
        self.score = 0
        self.sequential_victories = 0
        self.max_sequential_victories = 0
        self.history = []
    
    def for_dict(self):

        history_dict = []
        for h in self.history:
            history_dict.append(h.for_dict())

        return {

            "id": self.id,
            "name": self.name,
            "victories": self.victories,
            "defeats": self.defeats,
            "draws": self.draws,
            "score": self.score,
            "sequential_victories": self.sequential_victories,
            "max_sequential_victories": self.max_sequential_victories,
            "history": history_dict
        }

class Match:

    def __init__(self, id, player1_id, player2_id, draw, winner_id):
        self.id = id
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.draw = draw
        self.winner_id = winner_id
    
    def for_dict(self):
        return self.__dict__

class History:

    def __init__(self, match_id, oponent_id, oponent_name, result):
        self.match_id = match_id
        self.oponent_id = oponent_id
        self.oponent_name = oponent_name
        self.result = result
    
    def for_dict(self):
        return self.__dict__


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

            print("Preciso de um nome com no mínimo 3 caracteres para registrar.")
            print("Digite o nome do jogador:")
            name = input_validation_string(3)
            register_player(name)

        case "2":

            print("Preciso do id de dois jogadores para registrar a partida.")
            print('Digite o id do primeiro jogador: ')
            player1_id = input_validation_int()
            print('Digite o id do segundo jogador: ')
            player2_id = input_validation_int()
            register_match(player1_id, player2_id)

        case "3":

            print('Digite o id do jogador que deseja consultar:')
            id = input_validation_int()
            get_player(id)
            
        case "4":
            
            players = fetch_players()
            ranking_players(players)
            
            print('RANKING DE JOGADORES')
            print("\n" + "=" * 80)
            print(f"{'Posição':<10} {'Jogador':<20} {'Pontos':<10} {'Vitórias':<10} {'Empates':<10} {'Derrotas':<10}")
            print("=" * 80)
            for i in range(len(players)):

                print(
                    f"{i + 1:<10} "
                    f"{players[i].name:<20} "
                    f"{players[i].score:<10} "
                    f"{players[i].victories:<10} "
                    f"{players[i].draws:<10} "
                    f"{players[i].defeats:<10}"
                )
            print("=" * 80)

        case "5":

            players = fetch_players()
            total_players = len(players)
            total_matchs = len(fetch_matchs())
            player_more_sequential_vitories = get_player_more_sequential_victories()
            player_more_defeats = get_player_more_defeats()
            ranking_players(players)
            player_number_1 = players[0]


            with open(REPORT_ARCHIVE, "w", encoding="utf-8") as arquivo:

                arquivo.write("=============================================================================\n")
                arquivo.write("                           RELATÓRIO DO TORNEIO                              \n")
                arquivo.write("=============================================================================\n\n")
                
                arquivo.write(f"-> Total de jogadores cadastrados: {total_players}\n")
                arquivo.write(f"-> Total de partidas registradas: {total_matchs}\n")
                arquivo.write(f"-> Líder do ranking: {player_number_1.name} ({player_number_1.score} pontos)\n")
                arquivo.write(f"-> Jogador com mais derrotas: {player_more_defeats.name} ({player_more_defeats.defeats} derrotas)\n")
                arquivo.write(f"-> Maior sequência de vitórias: {player_more_sequential_vitories.name} ({player_more_sequential_vitories.max_sequential_victories} seguidas)\n\n")
                
                arquivo.write("=============================================================================\n")
                arquivo.write("                             RANKING GERAL                                   \n")
                arquivo.write("=============================================================================\n")
                
                template_tabela = "{:<5} | {:<15} | {:<10} | {:<10} | {:<10} | {:<10}\n"
                
                arquivo.write(template_tabela.format("POS", "NOME", "PONTOS", "VITÓRIAS", "EMPATES", "DERROTAS"))
                arquivo.write("-" * 77 + "\n")
                
                for i in range(len(players)):
                    arquivo.write(template_tabela.format(
                        f"{i + 1}º",
                        players[i].name,
                        players[i].score,
                        players[i].victories,
                        players[i].draws,
                        players[i].defeats
                    ))

            print("Relatório e ranking gerados com sucesso no arquivo 'relatorio.txt'!")

        case "6":

            system_on = False
            print("Você finalizou o sistema! Até mais!")

        case _:
            print('Digite um comando válido!')