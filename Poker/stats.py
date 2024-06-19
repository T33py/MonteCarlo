import Poker.pokerhands as poker
import Poker.card as card
players = 5
iterations = 10000000


def main():
    deck = poker.make_deck()
    poker.shuffle(deck)
    hands = [[]]
    for player in range(players):
        hands.append([])

    winner_counts = {}
    hand_type_counts = {}
    winning_hand_counts = {}

    for i in range(iterations):
        poker.deal(hands, deck)
        results = poker.identify_hands(hands)
        winners = poker.find_winners(results)
        _winners = [hands[results.index(winner)+1] for winner in winners]

        for hand in _winners:
            if hand[0].relative_strength < hand[1].relative_strength:
                fst = hand.pop(0)
                hand.append(fst)
            elif hand[0].relative_strength == hand[1].relative_strength:
                if hand[0].suit < hand[1].suit:
                    fst = hand.pop(0)
                    hand.append(fst)
            _hand = f'{hand[0]};{hand[1]}'
            if _hand in winner_counts:
                winner_counts[_hand] += 1
            else:
                winner_counts[_hand] = 1

        for hand in results:
            ht = hand[0]
            if ht in hand_type_counts:
                hand_type_counts[ht] += 1
            else:
                hand_type_counts[ht] = 1

        wht = winners[0][0]
        if wht in winning_hand_counts:
            winning_hand_counts[wht] += 1
        else:
            winning_hand_counts[wht] = 1

        poker.empty_hands(hands, deck)
        poker.shuffle(deck)
        if i%1000 == 0:
            print(f'{(i/iterations)*100:0.2f}%', end='\r')
    print()

    print(hand_type_counts)
    print(winning_hand_counts)

    ws = []
    cs = []
    sorted_ws = []
    sorted_cs = []

    for winner in winner_counts:
        ws.append(winner.replace('-', ';'))
        cs.append(winner_counts[winner])

    while len(ws) > 0:
        w = max(cs)
        widx = cs.index(w)
        sorted_ws.append(ws.pop(widx))
        sorted_cs.append(cs.pop(widx))
    
    with open('pokerdump.csv', 'a') as file:
        for i in range(len(sorted_ws)):
            file.write(f'{sorted_ws[i]};{sorted_cs[i]}\n')
    return

if __name__ == '__main__':
    main()
