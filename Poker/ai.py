import Poker.card as _card
import ai_index as index

BET = 'BET'
CALL = 'CALL'
FOLD = 'FOLD'
ALL_IN = 'ALL IN'


class Ai:
    def __init__(self):
        self.name: str = ''
        self.chips: int = 0
        self.chip_base_amount: int = 0
        self.chip_win_loss: int = 0
        self.current_big_blind: int = 0
        self.current_phase: int = index.PRE_FLOP
        self.weights: list[float] = []
        self.hand: list[_card.Card] = []

        # we want to relate each card to all other cards for each phase - setup list of ints long enough to hold all card combinations
        #  pre-flop
        #  flop
        #  turn
        #  river
        for p in range(4):
            for i in range(52):
                for j in range(52):
                    self.weights.append(1)
        for p in range(index.NUMBER_OF_PARAMETERS):
            self.weights.append(1)

    def make_decition(self, common_cards:list[_card.Card], to_call:int, pos:int):
        decition = FOLD
        chip_val = 0
        return [decition, chip_val]

    def card_weight(self, card:_card.Card, phase)->float:
        '''
        Weight of specified card for the current phase
        '''
        _suit = index.suits_index[card.suit]
        # ace has value = 1
        return self.weights[(card.value-1) + _suit + phase]
    
    def card_weight_based_on(self, card1:_card.Card, card2:_card.Card, phase)->float:
        '''
        Weight of the given card in combination with the provided card
        '''
        suit1 = index.suits_index[card1.suit]
        suit2 = index.suits_index[card2.suit]
        # ace has value = 1
        card1_idx = (card1.value-1) + suit1 + phase
        card2_idx = card1_idx + (52 * (card2.value-1 + suit2))
        return self.weights[card2_idx]
        return

    def change_chips(self, amount):
        '''
        change number of chips by the given amount
        '''
        self.chips += amount
        self.chip_win_loss += amount
        if self.chips <= 0:
            self.chips += self.chip_base_amount
        return

    def set_chip_base_amount(self, amount):
        '''
        set the base amount of chips, also changes the current number of chips
        '''
        self.chip_base_amount = amount
        self.chips = amount
        return

    def reset(self):
        self.chips = self.chip_base_amount
        self.chip_win_loss = 0
        self.current_phase = index.PRE_FLOP
        return

    def copy(self):
        '''
        Create a copy of this AI
        '''
        cp = Ai()
        cp.name = self.name
        cp.weights = self.weights.copy()
        cp.reset()
        return cp

    def serialize(self)->str:
        return str(self.weights)

    def __str__(self):
        return f'poker ai {self.name}'