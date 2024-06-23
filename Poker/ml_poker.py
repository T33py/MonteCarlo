from Poker.game import PokerGame
from Poker.ai import Ai
import random

iterations = 10000
files = 'test1'
games_to_run = 100
players_per_game = 5

def main():
    games:list[PokerGame] = []
    for i in range(games_to_run):
        game = PokerGame()
        game.number = i
        game.number_of_players = players_per_game
        game.verbose = False
        game.setup_players()
        for player in game.players:
            player.name = f'table {i} gen {0}'
        games.append(game)

    i = 0
    while i < iterations:
        for game in games:
            game.play_round()
        if i%1 == 0:
            print(f'{(i/iterations)*100:0.2f}%', end='\r')

        if i%1000 == 0:
            ais = list_ais(games)
            serialize(f'Poker/dump/{files}{i}.ai', ais)
            ais = sorted(ais, key=lambda ai: ai.chip_win_loss, reverse=True)
            stats_output(f'Poker/dump/{files}_stats.txt', ais, i)
            winners = ais[0:int((games_to_run*players_per_game)/4)]
            for ai in winners:
                ai.hard_reset()
            children = breed(winners)
            mutations = mutate(winners)
            next_gen = winners.copy()
            next_gen.extend(children)
            next_gen.extend(mutations)
            if len(next_gen) < games_to_run * players_per_game:
                next_gen.append(ais[0])
            populate_tables(next_gen, games)
        i += 1
    return

def populate_tables(ais: list[Ai], games: list[PokerGame]):
    for game in games:
        players = []
        for i in range(players_per_game):
            player = ais[random.randint(0,len(ais)-1)]
            players.append(player)
            ais.remove(player)
        game.players = players
    return

def breed(ais: list[Ai]):
    children = []
    i = 0
    for i in range(0, len(ais), 2):
        if i >= len(ais)-1:
            break

        ai1 = ais[i]
        ai1_name = ai1.name.split(' ')
        ai2 = ais[i+1]
        ai2_name = ai2.name.split(' ')
        child = ai1.copy()
        child.name = f'descended {ai1_name[1]},{ai2_name[1]} gen {int(ai1_name[3])+1}'
        for w in range(len(child.weights)):
            if random.uniform(-1,1) > 0:
                child.weights[w] = ai2.weights[w]
        children.append(child)
    return children

def mutate(ais: list[Ai]):
    mutations = []
    i = 0
    for i in range(len(ais)):
        child = ais[i].copy()
        for w in range(len(child.weights)):
            child.weights[w] += random.uniform(-1,1) * 0.1
            pn = ais[i].name.split(' ')
            child.name = f'mutated m{pn[1]} gen {int(pn[3])+1}'
        mutations.append(child)
    return mutations

def list_ais(games:list[PokerGame]) -> list[Ai]:
    ais = []
    for game in games:
        for ai in game.players:
            ais.append(ai)
    return ais

def serialize(filename, ais:list[Ai]):
    serialized = []
    for ai in ais:
        serialized.append(ai.serialize())
    
    with open(filename, 'a') as file:
        file.writelines(serialized)
    return

def stats_output(filename, ais:list[Ai], gen):
    stats = [f'#########gen{gen}#########']

    stats.append(f'ais: {len(ais)}')

    wls = [ai.chip_win_loss for ai in ais]
    gtz = 0
    for wl in wls:
        if wl > 0:
            gtz += 0
    wlstat = f'wl_max: {wls[0]}, wls>0: {gtz}, wl_min: {wls[len(wls)-1]}'
    stats.append(wlstat)

    stats.append(f'TOP10')
    for ai in ais[0:10]:
        stats.append(f'   {ai.name}: wl {ai.chip_win_loss}')

    stats = [f'##########################']
    with open(filename, 'a') as file:
        file.writelines(stats)
    return

if __name__ == "__main__":
    main()