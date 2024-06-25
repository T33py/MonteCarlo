from Poker.ai import Ai
from Poker.pokerhands import make_deck

file = f'Poker/dump/test6_53.ai'

def main():
    ais = deserialize_ais(file, 10)
    for ai in ais[0:10]:
        print(stringify_gto_chart(ai))

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

def stringify_gto_chart(ai:Ai)->str:
    string = ''
    chart = ai.generate_preflot_hand_chart(make_deck())
    for y in range(len(chart)):
        if y > 0:
            string += f'{chart[0][y]};'
        else:
            string += ';'
    for x in range(len(chart)):
        for y in range(len(chart[0])):
            if x > 0:
                thing = chart[x][y]
                if isinstance(thing, float):
                    thing = f'{thing:2.2}'
                string += f'{thing};'
        string += '\n'
    return string

if __name__ == '__main__':
    main()