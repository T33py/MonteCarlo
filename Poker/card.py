import random

cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
card_values = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13}
suits = ['H', 'D', 'S', 'K']
suit_names = {'H': 'Hearts', 'D': 'Diamonds', 'S': 'Spades', 'K': 'Klubs'}

class Card:

    def __init__(self):
        self.name = ''
        self.value = 0
        self.suit = ''
        self.relative_strength = 0

    def assign_random(self):
        self.name = cards[random.randint(0, len(cards)-1)]
        self.suit = suits[random.randint(0, len(suits)-1)]

    def long_str(self):
        return f'{self.name} of {suit_names[self.suit]}'

    def __str__(self):
        return f'{self.name}-{self.suit}'
    def __repr__(self) -> str:
        return self.__str__()
