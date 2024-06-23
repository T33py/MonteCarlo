import Poker.card as _card
import Poker.ai_index as index

BET = 'BET'
CALL = 'CALL'
CHECK = 'CHECK'
FOLD = 'FOLD'
ALL_IN = 'ALL IN'


class Ai:
    def __init__(self):
        self.name: str = ''
        self.chips: int = 0
        self.chip_base_amount: int = 0
        self.chip_win_loss: int = 0
        self.big_blind: int = 0
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

    def take_action(self, common_cards:list[_card.Card], pot, to_call:int, players:int, pos:int, raises:int, verbose:bool):
        decition = FOLD
        chip_val = 0
        hand_strength = self.calculate_handstrength(common_cards)
        remaining_chipcount_factor = self.weights[index.REMAINING_CHIPCOUNT_VALUE] * (self.chips/self.big_blind)
        pot_factor = self.weights[index.POT_SIZE_VALUE] * (pot/self.big_blind)
        needed_to_call_factor = self.weights[index.NEEDED_TO_CALL_MODIFIER] * (pot/self.big_blind)
        other_players_factor = self.weights[index.NUMBER_OF_OTHER_PLAYERS_MODIFIER] * players
        position_factor = self.weights[index.POSITION_MODIFIER] * pos
        raises_factor = self.weights[index.NUMBER_OF_RAISES_MODIFIER] * (raises * self.weights[index.NUMBER_OF_RAISES_MULTIPLIER])
        
        bet_size = self.big_blind * hand_strength
        bet_size *= pot_factor * needed_to_call_factor * other_players_factor * position_factor * raises_factor
        # only include chipcount in deliberations if it is big enough
        if self.weights[index.REMAINING_CHIPCOUNT_TO_BIGBLIND_CUTOFF] * self.big_blind >= self.chips:
            bet_size *= remaining_chipcount_factor

        ev = bet_size
        # setup bet in chips
        if self.chips-bet_size < self.weights[index.REMAINING_CHIPCOUNT_THRESHOLD] * self.big_blind:
            decition = ALL_IN
            bet_size = self.chips
        elif bet_size > to_call and bet_size >= self.big_blind:
            decition = BET
        elif to_call == 0 and self.weights[index.CHECK_CUTOFF] * self.big_blind > bet_size:
            decition = CHECK
            bet_size = 0
        else:
            decition = FOLD
            bet_size = 0
        
        chip_val = int(bet_size)
        if chip_val > 0 and chip_val < self.big_blind and self.chips >= self.big_blind:
            chip_val = self.big_blind

        if verbose:
            print(f'{self.name} decided to {decition} ({chip_val} chips) because {self.hand} and {common_cards} evaluated to {hand_strength} giving the hand an ev of {ev} with {to_call} to call')
        return [decition, chip_val]
    
    def calculate_handstrength(self, common_cards:list[_card.Card]):
        all_cards = [card for card in common_cards]
        all_cards.extend(self.hand)
        affinities = []
        for card1 in all_cards:
            for card2 in all_cards:
                if card1 != card2:
                    affinity = self.card_weight(card1, self.current_phase) * self.card_weight_based_on(card1, card2, self.current_phase)
                    affinities.append(affinity)
        return sum(affinities)

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
        if self.chips < 0:
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
        return f'Ai-{self.name}'
    def __repr__(self) -> str:
        return self.__str__()