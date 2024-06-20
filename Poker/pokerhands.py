from Poker.card import suit_names, card_values, Card, cards
import random

hand_names_by_relative_strength = ["high_card", "pair", "two_pair", "three_of_a_kind", "straight", "flush", "house", "four_of_a_kind", "straight_flush", "royal_straight_flush"]

players = 5
iterations = 100
def main():
    deck = make_deck()
    shuffle(deck)
    hands = [[]]
    for player in range(players):
        hands.append([])

    for i in range(iterations):
        deal(hands, deck)
        results = identify_hands(hands)
        winners = find_winners(results)
        _winners = [hands[results.index(winner)+1] for winner in winners]
        print("------")
        print(hands)
        print(results)
        print(winners)
        print(f'got {winners[0][0]}: {_winners}')
        print("------")
        empty_hands(hands, deck)
        shuffle(deck)
        input()
    
    return

def identify_hands(hands):
    '''
    Takes in a list of the hands to identify based on the common cards that should be placed as the first item in the list. [[*common_cards*], [*hand1*], [*hand2*], etc.]
    Returns a list of resulting hands with 2 items ["name of hand", [*cards that make up the strongest poker hand*], [*cards that give the hand its name*]] for each hand
    '''
    result = []
    for hand in hands[1:]:
        result.append(identify_hand(hand, hands[0]))
    return result

def identify_hand(hand: list[Card], common_cards: list[Card]):
    '''
    Takes in a list of cards in the players hand, and a list of common cards (assumed to be 5 long).
    Returns a list with 2 items ["name of hand", [*cards that make up the strongest poker hand*], [*cards that give the hand its name*]]
    '''
    values = {}
    values_cards = {}
    suits = {}
    suits_cards = {}
    add_cards_to_dicts(hand, values, values_cards, suits, suits_cards)
    add_cards_to_dicts(common_cards, values, values_cards, suits, suits_cards)
    hand_is = hand_names_by_relative_strength[0]
    
    # # of a kind
    pairs = 0
    pairs_cards = []
    threes = 0
    threes_cards = []
    fours = 0
    fours_cards = []
    for value in values:
        if values[value] == 2:
            pairs += 1
            pairs_cards.append(values_cards[value])
        elif values[value] == 3:
            threes += 1
            threes_cards.append(values_cards[value])
        elif values[value] == 4:
            fours += 1
            fours_cards.append(values_cards[value])
    
    # straight
    is_straight = False
    is_royal = False
    vals_sort = sorted(values)
    lst = vals_sort[0]
    straight = 1 # the card we are looking at counts towards the current straight check
    straight_cards = []
    has_ace = False
    for val in vals_sort:
        # do the thing
        straight_cards.append(values_cards[val][0])
        if val - lst < 0 or val - lst > 1:
            straight = 1
            if not is_straight:
                straight_cards = [values_cards[val][0]]
        elif val - lst == 1:
            straight += 1
        lst = val
        
        # fix the edgecases
        if val == 1: # if val is ace do something to fix for king
            has_ace = True
        if val == 13 and has_ace and straight >= 4: # if there is an ace and the current card is a king - the ace should count in the straight
            straight += 1
            straight_cards.append(values_cards[1][0])
            is_royal = True
        if straight >= 5:
            is_straight = True

        if len(straight_cards) > 5:
            if straight < len(straight_cards): # this is only true when the current card is higher than, but not part of, the straight we found
                straight_cards.pop(len(straight_cards)-1)
            else:
                straight_cards.pop(0) 

    # flush
    is_flush = False
    flush_cards = []
    for suit in suits:
        if suits[suit] >= 5:
            is_flush = True
            flush_cards = suits_cards[suit]
    
    if is_flush:
        flush_cards = sorted(flush_cards, key=lambda c: c.relative_strength)
        while flush_cards[0].value == 1:
            c = flush_cards.pop(0)
            flush_cards.append(c)
        while len(flush_cards) > 5:
            flush_cards.pop(0)

    cards_that_is_in_hand = []

    # what hand do we have
    pairs_cards = sorted(pairs_cards, key=lambda p: p[0].relative_strength)
    if pairs == 1:
        hand_is = hand_names_by_relative_strength[1]
        # print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
        cards_that_is_in_hand = pairs_cards[0]
    elif pairs >= 2:
        hand_is = hand_names_by_relative_strength[2]
        # print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
        while len(pairs_cards) > 2:
            pairs_cards.pop(0)
        for pair in pairs_cards:
            for card in pair:
                cards_that_is_in_hand.append(card)
        
    threes_cards = sorted(threes_cards, key=lambda p: p[0].relative_strength)
    if threes > 0:
        hand_is = hand_names_by_relative_strength[3]
        # print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
        cards_that_is_in_hand = []
        if len(threes_cards) == 1:
            cards_that_is_in_hand = threes_cards[0]
        elif threes_cards[0][0].relative_strength > threes_cards[1][0].relative_strength:
            cards_that_is_in_hand = threes_cards[0]
        else:
            cards_that_is_in_hand = threes_cards[1]
            
    
    if is_straight:
        hand_is = hand_names_by_relative_strength[4]
        # print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
        cards_that_is_in_hand = []
        cards_that_is_in_hand = straight_cards

    if is_flush:
        hand_is = hand_names_by_relative_strength[5]
        # print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
        cards_that_is_in_hand = []
        cards_that_is_in_hand = flush_cards
    

    if (threes > 0 and pairs > 0) or threes == 2:
        hand_is = hand_names_by_relative_strength[6]
        # print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
        cards_that_is_in_hand = []
        pair = []
        three = []
        if pairs > 0:
            pair = pairs_cards[len(pairs_cards)-1]
            three = threes_cards[0]
        else:
            three = threes_cards[1]
            pair.append(threes_cards[0][0])
            pair.append(threes_cards[0][1])
        cards_that_is_in_hand.append(pair[0])
        cards_that_is_in_hand.append(pair[1])
        cards_that_is_in_hand.append(three[0])
        cards_that_is_in_hand.append(three[1])
        cards_that_is_in_hand.append(three[2])

    if fours > 0:
        hand_is = hand_names_by_relative_strength[7]
        # print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
        cards_that_is_in_hand = []
        cards_that_is_in_hand = fours_cards[0]
    
    if is_straight and is_flush:
        suit = flush_cards[0].suit
        found_replacements = True
        for i in range(len(straight_cards)):
            replaced = True
            card: Card = straight_cards[i]
            if card.suit != suit:
                replaced = False
                for c in values_cards[card.value]:
                    if c.suit == suit:
                        straight_cards[i] = c
                        replaced = True
            if not replaced:
                found_replacements = False

        if found_replacements:
            hand_is = hand_names_by_relative_strength[8]
            # print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
            cards_that_is_in_hand = []
            cards_that_is_in_hand = straight_cards
        else:
            is_straight = False


    if is_royal and is_straight and is_flush:
        hand_is = hand_names_by_relative_strength[9]
        # should be the straight flush from "straight flush check"

    cards_that_define_hand = cards_that_is_in_hand.copy()

    # backfill with strongest kicker
    all_cards = []
    all_cards.extend(hand)
    all_cards.extend(common_cards)
    all_cards = sorted(all_cards, key=lambda p: p.relative_strength, reverse=True)
    while len(cards_that_is_in_hand) < 5:
        for card in all_cards:
            if not (card in cards_that_is_in_hand):
                cards_that_is_in_hand.append(card)
                break

    # order cards by relative strenght
    cards_that_define_hand = sorted(cards_that_define_hand, key=lambda p: p.relative_strength, reverse=True)
    cards_that_is_in_hand = sorted(cards_that_is_in_hand, key=lambda p: p.relative_strength, reverse=True)
    return [hand_is, cards_that_is_in_hand, cards_that_define_hand]

def find_winners(hands):
    '''
    compile a list of the winning hands from the output of identify hands. If there are multiple winners their hands have the same strength.
    '''
    hands_by_hand_strength = sorted(hands, key=lambda r: hand_names_by_relative_strength.index(r[0]), reverse=True)
    winning_hand_name = hands_by_hand_strength[0][0]
    winning_hands = []
    
    # Find same hand name with different cards
    candidates = []
    for hand in hands_by_hand_strength:
        if hand[0] == winning_hand_name:
            candidates.append(hand)

    # high card
    if winning_hand_name == hand_names_by_relative_strength[0]:
        # high card wins
        # cards are sorted, so we just choose the ones with the biggest number
        for i in range(5):
            remove_if_not_best_kicker(candidates, i)
        winning_hands.extend(candidates)

    # pair / two pair
    elif winning_hand_name == hand_names_by_relative_strength[1] or winning_hand_name == hand_names_by_relative_strength[2]:
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
        
        if winning_hand_name == hand_names_by_relative_strength[1]:
            for i in range(3,5):
                remove_if_not_best_kicker(winning_hands, i)
        else:
            remove_if_not_best_kicker(winning_hands, 4)

    # 3 of a kind
    elif winning_hand_name == hand_names_by_relative_strength[3]:
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
        remove_if_not_best_kicker(winning_hands, 3)
        remove_if_not_best_kicker(winning_hands, 4)
        

    # straight
    elif winning_hand_name == hand_names_by_relative_strength[4]:
        # cards are ordered by relative strength - so any straight that is bigger should have a larger card in the middle.
        # because As have relative strength 14 first and last card breaks if there is an ace.
        sorted_straights = sorted(candidates, key=lambda c: c[1][2].relative_strength, reverse=True)
        biggest_mid = sorted_straights[0][1][2].relative_strength 
        for straight in sorted_straights:
            if straight[1][2].relative_strength == biggest_mid:
                winning_hands.append(straight)

    # flush
    elif winning_hand_name == hand_names_by_relative_strength[5]:
        # high card wins
        # cards are sorted, so we just choose the ones with the biggest numbers
        for i in range(5):
            remove_if_not_best_kicker(candidates, i)
        winning_hands.extend(candidates)

    # house
    elif winning_hand_name == hand_names_by_relative_strength[6]:
        # as there are 5 cards it's a pair an a 3, so we organize them [[*pair*], [*3*]]
        threes = [find_3_of(house[1]) for house in candidates]
        max3 = max(threes)
        to_remove = []
        for i in range(len(candidates)):
            if threes[i] != max3:
                to_remove.append(i)

        to_remove.reverse() # reverse to remove from the back
        for idx in to_remove:
            candidates.pop(idx)
        to_remove.clear()

        if len(candidates) > 1:
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
    elif winning_hand_name == hand_names_by_relative_strength[7]:
        # there will only be 1 kind with more than 1 so pairs will return [[*4*], [*kicker*]]
        fours = [find_pairs(hand[1]) for hand in candidates]
        pairs = [four[0][0] for four in fours]
        max4 = max(pairs)
        to_remove = []
        for i in range(len(candidates)):
            if pairs[i] != max4:
                to_remove.append(i)
        to_remove.reverse()
        for idx in to_remove:
            candidates.pop(idx)
        to_remove.clear()

        remove_if_not_best_kicker(candidates, 4)
        winning_hands.extend(candidates)

    # straight flush
    # royal straight flush
    elif winning_hand_name == hand_names_by_relative_strength[8] or winning_hand_name == hand_names_by_relative_strength[9]:
        # biggest straight wins - royal straight flush is the biggest straight flush
        sorted_straights = sorted(candidates, key=lambda c: c[1][2].relative_strength, reverse=True)
        biggest_mid = sorted_straights[0][1][2].relative_strength 
        for straight in sorted_straights:
            if straight[1][2].relative_strength == biggest_mid:
                winning_hands.append(straight)
            
    return winning_hands

def remove_if_not_best_kicker(hands:list, card_number:int):
    '''
    if the card at "card_number" isn't equal to the best kicker among the hands given, the hand is removed from the list of hands ("card_number" is 0 indexed)
    '''
    vals = [h[1][card_number].relative_strength for h in hands]
    max_kicker = max(vals)
    to_remove = []
    for i in range(len(hands)):
        if hands[i][1][card_number].relative_strength < max_kicker:
            to_remove.append(i)
    to_remove.reverse()
    for idx in to_remove:
        hands.pop(idx)
    return

def find_card_that_does_not_have_value(hand, value):
    '''
    find a card with a value that is not the one provided and return the value of the card found
    '''
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

def find_pairs(hand: list[Card]):
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

def add_cards_to_dicts(cards, values, values_cards, suits, suits_cards):
    for c in cards:
        ca: Card = c
        if ca.value in values:
            values[ca.value] += 1
            values_cards[ca.value].append(ca)
        else:
            values[ca.value] = 1
            values_cards[ca.value] = [ca]
        if ca.suit in suits:
            suits[ca.suit] += 1
            suits_cards[ca.suit].append(ca)
        else:
            suits[ca.suit] = 1
            suits_cards[ca.suit] = [ca]
    return

def deal(hands, deck):
    '''
    Deal cards from the deck to the hands according to texas holdem rules.
    hands[0] is treated as the common cards.
    '''
    for c in range(2):
        for h in range(1, len(hands)):
            hands[h].append(draw(deck))

    for c in range(5):
        hands[0].append(draw(deck))
    return

def empty_hands(hands:list, deck:list):
    '''
    Move all cards from the hands to the deck.
    '''
    for hand in hands:
        for card in hand:
            deck.append(card)
        hand.clear()
    return

def draw(deck:list)-> Card:
    '''
    Draw the top card from the deck
    '''
    card = deck[0]
    deck.remove(card)
    return card

def shuffle(deck:list):
    '''
    Randomize the order of the cards in the deck
    '''
    shuffled = []
    while len(deck) > 0:
        idx = random.randint(0, len(deck)-1)
        c = deck[idx]
        shuffled.append(c)
        deck.remove(c)

    for c in shuffled:
        deck.append(c)
    return

def make_deck()->list[Card]:
    '''
    Setup a default 52 card poker deck
    '''
    deck = []
    for suit in suit_names:
        for name in cards:
            c = Card()
            c.name = name
            c.suit = suit
            c.value = card_values[name]
            c.relative_strength = card_values[c.name]
            if c.value == 1:
                c.relative_strength = 14
            deck.append(c)
    return deck

if __name__ == '__main__':
    main()