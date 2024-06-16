import Poker.pokerhands as poker
import Poker.card as card
players = 5
iterations = 1000000


def main():
    deck = poker.make_deck()
    poker.shuffle(deck)
    hands = [[]]
    for player in range(players):
        hands.append([])

    for i in range(iterations):
        poker.deal(hands, deck)
        results = poker.identify_hands(hands)
        winners = poker.find_winners(results)
        print("------")
        print(hands)
        print(results)
        print(winners)
        _winners = [hands[results.index(winner)+1] for winner in winners]
        print(f'winner: {winners[0][0]} {_winners}')
        print("------")
        poker.empty_hands(hands, deck)
        poker.shuffle(deck)
        input()
    
    return

if __name__ == '__main__':
    main()
