from Poker.ai import Ai
from Poker.pokerhands import make_deck

file = f'Poker/dump/test199.ai'

def main():
    ais = deserialize_ais(file)
    for ai in ais[0:10]:
        chart = ai.generate_preflot_hand_chart(make_deck())
        for y in range(len(chart)):
            if y > 0:
                print(f'{chart[0][y]}   ', end='')
            else:
                print('     ', end='')
        print('')
        for x in range(len(chart)):
            for y in range(len(chart[0])):
                if x > 0:
                    thing = chart[x][y]
                    if isinstance(thing, float):
                        thing = f'{thing:2.2}'
                    while len(thing) < 4:
                        thing = thing + ' '
                        
                    print(f'{thing} ', end='')
            print('')
        print('\n')

    return

def deserialize_ais(filepath:str, number:int=-1)-> list[Ai]:
    ais = []
    with open(filepath) as file:
        str_ais = file.readlines()
        if number < 0:
            number = len(str_ais)
        for str_ai in str_ais:
            ai = Ai()
            ai.deserialize(str_ai)
            ais.append(ai)
            if len(ais) == number:
                break
    return ais

if __name__ == '__main__':
    main()