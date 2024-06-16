import Poker.pokerhands as pokerhands
import Poker.card as card
players = 5
iterations = 1000000


def main():
    deck = pokerhands.make_deck()
    pokerhands.shuffle(deck)
    hands = [[]]
    for player in range(players):
        hands.append([])

    for i in range(iterations):
        pokerhands.deal(hands, deck)
        results = pokerhands.identify_hands(hands)
        print("------")
        print(hands)
        print(results)
        print("------")
        pokerhands.empty_hands(hands, deck)
        pokerhands.shuffle(deck)
        input()
    
    return

def find_strongest_hand(hands):
    hands_by_hand_strength = sorted(hands, key=lambda r: pokerhands.hand_names_by_relative_strength.index(r[0]), reverse=True)
    return

if __name__ == '__main__':
    main()
