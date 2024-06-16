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
        winners = find_winners(results)
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

def find_winners(hands):
    '''
    compile a list of the winning hands
    '''
    hands_by_hand_strength = sorted(hands, key=lambda r: poker.hand_names_by_relative_strength.index(r[0]), reverse=True)
    winning_hand_name = hands_by_hand_strength[0][0]
    winning_hands = []
    
    # Find same hand name with different cards
    candidates = []
    for hand in hands_by_hand_strength:
        if hand[0] == winning_hand_name:
            candidates.append(hand)

    # high card
    if winning_hand_name == poker.hand_names_by_relative_strength[0]:
        # high card wins
        # cards are sorted, so we just choose the ones with the biggest number
        for i in range(len(candidates[0][1])):
            vals = [c[1][i].relative_strength for c in candidates]
            m = max(vals)
            for c in range(len(vals)):
                if vals[c] < m:
                    candidates.pop(c)
        winning_hands.append(candidates)

    # pair / two pair
    elif winning_hand_name == poker.hand_names_by_relative_strength[1] or winning_hand_name == poker.hand_names_by_relative_strength[2]:
        pairs = [find_pairs(hand[1]) for hand in candidates]
        # a pair is [[*pairs*], [*kickers*]] represented by their size
        best_pair = pairs[0]
        for i in range(len(pairs)):
            pair = pairs[i]
            cmp = is_better_pair(pair, best_pair)
            if cmp == 1:
                winning_hands.clear()
                winning_hands.append(candidates[i])
                best_pair = pair
            if cmp == 0:
                winning_hands.append(candidates[i])

    # 3 of a kind
    elif winning_hand_name == poker.hand_names_by_relative_strength[3]:
        best3 = candidates[0]
        best3_val = find_3_of(best3[1])
        for i in range(len(candidates)):
            val = find_3_of(candidates[i][1])
            if val > best3_val:
                winning_hands.clear()
                winning_hands.append(candidates[i])
                best3 = candidates[i]
                best3_val = val
            elif val == best3_val:
                winning_hands.append(candidates[i])



    # straight
    elif winning_hand_name == poker.hand_names_by_relative_strength[4]:
        # cards are ordered by relative strength - so any straight that is bigger should have a larger card in the middle.
        # because As have relative strength 14 first and last card breaks if there is an ace.
        sorted_straights = sorted(candidates, key=lambda c: c[1][2].relative_strength, reverse=True)
        biggest_mid = sorted_straights[0][1][2].relative_strength 
        for straight in sorted_straights:
            if straight[1][2].relative_strength == biggest_mid:
                winning_hands.append(straight)

    # flush
    elif winning_hand_name == poker.hand_names_by_relative_strength[5]:
        # high card wins
        # cards are sorted, so we just choose the ones with the biggest numbers
        for i in range(len(candidates[0][1])):
            cs_to_discard = []
            vals = [c[1][i].relative_strength for c in candidates]
            m = max(vals)
            for c in range(len(vals)):
                if vals[c] < m:
                    cs_to_discard.append(c)
            for c in cs_to_discard:
                candidates.pop(c)
        winning_hands.extend(candidates)


    # house
    elif winning_hand_name == poker.hand_names_by_relative_strength[6]:
        # as there are 5 cards it's a pair an a 3, so we organize them [[*pair*], [*3*]]
        threes = [find_3_of(house[1]) for house in candidates]
        max3 = max(threes)
        to_remove = []
        for i in range(len(candidates)):
            if threes[i] != max3:
                to_remove.append(i)

        print(f'  {to_remove}')
        to_remove.reverse() # reverse to remove from the back
        for idx in to_remove:
            candidates.pop(idx)
        to_remove.clear()

        if len(candidates) > 1:
            print(candidates)
            # if there are more than 1 we need to find the pairs
            pairs = [find_card_that_does_not_have_value(house[1], max3) for house in candidates]
            max_pair = max(pairs)
            for i in range(len(candidates)):
                if pairs[i] != max_pair:
                    to_remove.append(i)
            to_remove.reverse() # reverse to remove from the back
            for idx in to_remove:
                candidates.pop(idx)
                
        winning_hands.extend(candidates)

    # 4 of a kind
    elif winning_hand_name == poker.hand_names_by_relative_strength[7]:
        # there will only be 1 kind with more than 1 so pairs will return [[*4*], [*kicker*]]
        fours = [find_pairs(hand[1]) for hand in candidates]
        pairs = [four[0][0] for four in fours]
        max4 = max(pairs)
        for i in range(len(candidates)):
            if pairs[i] != max4:
                candidates.pop(i)
                pairs.pop(i)

        if len(candidates) > 1:
            kickers = [four[1][0] for four in fours]
            max_kicker = max(kickers)
            for i in range(len(candidates)):
                if kickers[i] != max_kicker:
                    candidates.pop(i)
                    pairs.pop(i)
                    kickers.pop(i)
        winning_hands.extend(candidates)

    # straight flush
    # royal straight flush
    elif winning_hand_name == poker.hand_names_by_relative_strength[8] or winning_hand_name == poker.hand_names_by_relative_strength[9]:
        # biggest straight wins - royal straight flush is the biggest straight flush
        sorted_straights = sorted(candidates, key=lambda c: c[1][2].relative_strength, reverse=True)
        biggest_mid = sorted_straights[0][1][2].relative_strength 
        for straight in sorted_straights:
            if straight[1][2].relative_strength == biggest_mid:
                winning_hands.append(straight)
            
    return winning_hands

def find_card_that_does_not_have_value(hand, value):
    val = 0
    for c in hand:
        if c.relative_strength != value:
            val = c.relative_strength
            break
    return val

def find_3_of(hand)-> int:
    '''
    returns the value of the card there is 3 of
    '''
    count = {}
    for card in hand:
        if card.relative_strength in count:
            count[card.relative_strength] += 1
        else:
            count[card.relative_strength] = 1
    
    val = 0
    for c in count:
        if c == 3:
            val = c
    return val

def is_better_pair(pair1:list, pair2:list):
    '''
    compares the output of find_pairs and returns 1 if left is better, 0 if they are the same and -1 if right is better
    '''
    for i in range(len(pair1[0])):
        if pair1[0][i] > pair2[0][i]:
            return 1
        if pair1[0][i] < pair2[0][i]:
            return -1
    for i in range(len(pair1[1])):
        if pair1[1][i] > pair2[1][i]:
            return 1
        if pair1[1][i] < pair2[1][i]:
            return -1
    return 0

def find_pairs(hand: list[card.Card]):
    '''
    turn a hand into [[*pairs value*], [*kickers*]], ex [1,1,2,3,4] -> [[1], [2,3,4]], [1,1,2,2,3] -> [[1, 2], [3]]
    '''
    pairs = []
    kickers = []
    for card in hand:
        if card.relative_strength in kickers:
            pairs.append(card.relative_strength)
            kickers.remove(card.relative_strength)
        elif card.relative_strength not in pairs:
            kickers.append(card.relative_strength)
    
    pairs = sorted(pairs, reverse=True)
    kickers = sorted(kickers, reverse=True)
    return [pairs, kickers]

if __name__ == '__main__':
    main()
