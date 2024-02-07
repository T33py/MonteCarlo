import random
from BlackJack.card_util import cards, suits, card

class black_jack:
    def __init__(self):
        '''
        A game of blackjack with a single shuffled deck of cards
        '''
        self.card_value = {
            'A': [1, 11], 
            '2': 2, 
            '3': 3, 
            '4': 4, 
            '5': 5, 
            '6': 6, 
            '7': 7, 
            '8': 8, 
            '9': 9, 
            '10': 10, 
            'J': 10, 
            'Q': 10, 
            'K': 10,
        }

        self.black_jack_payrate = 3/2

        self.hands = []
        self.bets = []
        self.dealers_hand = []
        
        self.template_deck = []
        for c in cards:
            for s in suits:
                _card = card()
                _card.name = c
                _card.suit = s
                _card.value = self.card_value[_card.name]
                self.template_deck.append(_card)
        
        self.card_index = 0
        self.deck = self.new_deck()

    def deal(self, hands:int, bets:list, remove_cards:bool = False):
        '''
        Deal a new set of hands, and deal new cards to the dealer.
        '''
        self.hands.clear()
        self.bets = bets
        self.dealers_hand.clear()
        
        for i in range(hands):
            hand = [self.next_card(remove_cards), self.next_card(remove_cards)]
            self.hands.append(hand)
        self.dealers_hand = [self.next_card(), self.next_card()]

        return self.hands
    
    def hand_value(self, hand:list):
        '''
        calculate the value of a hand
        '''
        val = 0
        As = 0
        for c in hand:
            if c.name == 'A':
                if val + c.value[1] > 21:
                    val += c.value[0]
                else:
                    val += 11
                    As += 1
            else:
                val += c.value
                # if we counted any aces for 11 and we bust we can count them as 1s (11-10)
                while val > 21 and As > 0:
                    val -= 10
                    As -= 1
        return val
    
    def hit(self, hand:list, remove_card:bool = False):
        '''
        Add the next card to the hand
        '''
        hand.append(self.next_card(remove_card))

    def play_dealer(self, remove_cards:bool = False):
        '''
        Run the dealers turn with the "hit on 16 / stand on 17" rules
        '''
        while self.hand_value(self.dealers_hand) < 17:
            self.dealers_hand.append(self.next_card(remove_cards))

        return self.hand_value(self.dealers_hand)


    def next_card(self, remove:bool = False, shuffle:bool = True):
        '''
        Deal the next card
        '''
        if remove and len(self.deck) == 0:
            raise ValueError('Not enough cards to deal')
        card = self.deck[self.card_index]
        if remove:
            self.deck.remove(card)
        else:
            self.card_index = (self.card_index + 1) % len(self.deck)
        if shuffle:
            if self.card_index == 0:
                self.shuffle(self.deck)
        return card

    def winner(self, hand:list):
        '''
        Determine whether the provided hand wins against the dealers hand.
        If the hand wins 1 is returned.
        If the dealer wins -1 is returned.
        If its a push 0 is returned
        '''
        ds = self.hand_value(self.dealers_hand)
        hs = self.hand_value(hand)
        #black jack = 2 to 1
        if len(hand) == 2 and hs == 21:
            return self.black_jack_payrate
        if hs > 21:
            return -1
        if ds > 21:
            return 1
        if ds > hs:
            return -1
        if hs > ds:
            return 1
        return 0

    def shuffle(self, deck):
        '''
        Shuffle the deck
        '''
        random.shuffle(deck)

    def new_deck(self):
        '''
        Generate a new shuffled deck
        '''
        deck = self.template_deck.copy()
        self.shuffle(deck)
        return deck
    
