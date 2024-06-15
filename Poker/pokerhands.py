from Poker.card import suit_names, card_values, Card, cards
import random
players = 10
iterations = 10000000

def main():
    deck = make_deck()
    shuffle(deck)
    hands = [[]]
    for player in range(players):
        hands.append([])

    for i in range(iterations):
        deal(hands, deck)
        results = identify_hands(hands)
        print("------")
        print(hands)
        print(results)
        print("------")
        empty_hands(hands, deck)
        shuffle(deck)
        input()
    
    return

def identify_hands(hands):
    result = []
    for hand in hands[1:]:
        result.append(identify_hand(hand, hands[0]))
    return result

def identify_hand(hand, common_cards):
    values = {}
    values_cards = {}
    suits = {}
    suits_cards = {}
    add_cards_to_dicts(hand, values, values_cards, suits, suits_cards)
    add_cards_to_dicts(common_cards, values, values_cards, suits, suits_cards)
    hand_is = "high card"
    
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
        if val == 13 and has_ace: # if there is an ace and the current card is a king - the ace should count in the straight
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

    is_flush = False
    flush_cards = []
    for suit in suits:
        if suits[suit] >= 5:
            is_flush = True
            flush_cards = suits_cards[suit]
    
    flush_cards = sorted(flush_cards, key=lambda c: c.value)
    while len(flush_cards) > 5:
        flush_cards.pop(0)

    cards_that_is_in_hand = []

    pairs_cards = sorted(pairs_cards, key=lambda p: p[0].value)
    if pairs == 1:
        hand_is = "pair"
        print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
        cards_that_is_in_hand = pairs_cards[0]
    elif pairs >= 2:
        hand_is = "two_pair"
        print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
        while len(pairs_cards) > 2:
            pairs_cards.pop(0)
        for pair in pairs_cards:
            for card in pair:
                cards_that_is_in_hand.append(card)
        
    threes_cards = sorted(threes_cards, key=lambda p: p[0].value)
    if threes > 0:
        hand_is = "three_of_a_kind"
        print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
        cards_that_is_in_hand = []
        if len(threes_cards) == 1:
            cards_that_is_in_hand = threes_cards[0]
        elif threes_cards[0][0].value > threes_cards[1][0].value:
            cards_that_is_in_hand = threes_cards[0]
        else:
            cards_that_is_in_hand = threes_cards[1]
            
    
    if is_straight:
        hand_is = "straight"
        print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
        cards_that_is_in_hand = []
        cards_that_is_in_hand = straight_cards

    if is_flush:
        hand_is = "flush"
        print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
        cards_that_is_in_hand = []
        cards_that_is_in_hand = flush_cards
    

    if (threes > 0 and pairs > 0) or threes == 2:
        hand_is = "house"
        print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
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
        hand_is = "four_of_a_kind"
        print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
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
            hand_is = "straight_flush"
            print(f"{hand_is}: {hand} {common_cards} | {values_cards}, {suits_cards}")
            cards_that_is_in_hand = []
            cards_that_is_in_hand = straight_cards


    if is_royal and is_straight and is_flush:
        hand_is = "royal_straight_flush"
        # should be the straight flush from "straight flush check"

    return [hand_is, cards_that_is_in_hand]

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
    for c in range(2):
        for h in range(1, len(hands)):
            hands[h].append(draw(deck))

    for c in range(5):
        hands[0].append(draw(deck))
    return

def empty_hands(hands:list, deck:list):
    for hand in hands:
        for card in hand:
            deck.append(card)
        hand.clear()
    return

def draw(deck:list):
    card = deck[0]
    deck.remove(card)
    return card

def shuffle(deck:list):
    shuffled = []
    while len(deck) > 0:
        idx = random.randint(0, len(deck)-1)
        c = deck[idx]
        shuffled.append(c)
        deck.remove(c)

    for c in shuffled:
        deck.append(c)
    return

def make_deck():
    deck = []
    for suit in suit_names:
        for name in cards[6:]:
            c = Card()
            c.name = name
            c.suit = suit
            c.value = card_values[name]
            deck.append(c)
    return deck

if __name__ == '__main__':
    main()