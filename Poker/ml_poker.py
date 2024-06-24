from Poker.game import PokerGame
from Poker.ai import Ai
import random

generations = 100
iterations_per_gen = 1000
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

    iters = generations * iterations_per_gen
    icount = 0
    for g in range(generations):
        for i in range(iterations_per_gen):
            for game in games:
                game.play_round()
            icount += 1
            if icount%100 == 0:
                print(f'{(icount/iters)*100:0.2f}%', end='\r')

        ais = list_ais(games)
        ais = sorted(ais, key=lambda ai: ai.chip_win_loss, reverse=True)
        serialize(f'Poker/dump/{files}_{g}.ai', ais)
        stats_output(f'Poker/dump/{files}_stats{g}.txt', ais, g)
        winners = ais[0:int((games_to_run*players_per_game)/4)]
        for ai in winners:
            ai.hard_reset()
        children = breed(winners)
        mutations = mutate(winners)
        next_gen = winners.copy()
        next_gen.extend(children)
        next_gen.extend(mutations)
        while len(next_gen) < games_to_run * players_per_game: # just get some random ones, just in case they we hit by bad variance
            next_gen.append(ais[random.randint(0,len(ais)-1)])
        populate_tables(next_gen, games)
        g += 1
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
        child.name = f'descended {min([ai1_name[3], ai2_name[3]])} gen {int(ai1_name[3])+1}'
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
        serialized.append(ai.serialize()+'\n')
    
    with open(filename, 'a') as file:
        file.writelines(serialized)
    return

def stats_output(filename, ais:list[Ai], gen):
    stats = [f'#########gen{gen}#########\n']

    stats.append(f'ais: {len(ais)}\n')

    wls = [ai.chip_win_loss for ai in ais]
    gtz = 0
    for wl in wls:
        if wl > 0:
            gtz += 1
    wlstat = f'wl_max: {wls[0]}, wls>0: {gtz}, wl_min: {wls[len(wls)-1]}\n'
    stats.append(wlstat)

    stats.append(f'TOP10\n')
    for ai in ais[0:10]:
        stats.append(f'   {ai.name}: wl {ai.chip_win_loss}\n')

    stats.append(f'##########################\n')
    with open(filename, 'a') as file:
        file.writelines(stats)
    return

if __name__ == "__main__":
    main()