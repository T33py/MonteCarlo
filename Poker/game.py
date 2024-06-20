from Poker.pokerhands import make_deck, shuffle, draw, empty_hands, identify_hands, find_winners
from Poker.ai import Ai, BET, CALL, CHECK, FOLD, ALL_IN
import Poker.ai_index as ai_index
import Poker.card as card
import random

def main():
    game = PokerGame()
    game.setup_players()
    print(f'players {game.players}')

    game.play_round()


    return

class PokerGame:
    number_of_players = 5
    starting_chips: int = 1000
    big_blind: int = 10
    small_blind: int = 5

    deck: list[card.Card] = []
    players: list[Ai] = []
    common_cards: list[card.Card] = []
    hands: list[list[card.Card]] = []
    currently_playing: list[Ai] = []

    number_of_raises: int = 0
    to_call: int = 0
    last_bet: int = 0
    last_better: Ai
    turn: int = 0

    def __init__(self):
        self.deck = make_deck()
        shuffle(self.deck)

    def play_round(self):
        # setup
        self.hands = [p.hand for p in self.players]
        self.hands.insert(0, self.common_cards)
        self.currently_playing = [p for p in self.players]
        pots:list[int] = [ 0 ]
        players_in_pots = [self.currently_playing]
        print(f'players at table {self.players}')
        print(f'set up to play {self.currently_playing}')

        # play
        print('preflop setup')
        self.preflop(pots, players_in_pots)
        print('preflop play')
        self.do_play(pots, players_in_pots)

        # clean up
        empty_hands(self.hands, self.deck)
        shuffle(self.deck)

        # move button
        p = self.players.pop(0)
        self.players.append(p)

        # rebuy
        for player in self.players:
            if player.chips == 0:
                player.chips += player.chip_base_amount
        return

    def do_play(self, pots:list[int], players_in_pots):
        print(f'playing with {self.currently_playing}')
        has_action = [True for player in self.currently_playing]
        while self.more_actions(has_action):
            player = self.currently_playing[self.turn]
            if player.chips > 0:
                print(f'its {player.name}s turn')
                action = player.take_action(self.hands[0], sum(pots), self.to_call, len(self.currently_playing), self.turn, self.number_of_raises, True)
                if action[0] == FOLD:
                    self.currently_playing.pop(self.turn)
                    has_action.pop(self.turn)
                elif action[0] == BET:
                    self.allow_actions(has_action)
                    has_action[self.turn] = False
                    bet = action[1]
                    player.change_chips(-bet)
                    pots[0] += bet
                    diff = bet - self.last_bet
                    self.to_call += diff
                    self.last_bet = diff
                    self.last_better = player
                    self.number_of_raises += 1
                elif action[0] == CALL:
                    has_action[self.turn] = False
                    pots[0] += action[1]
                    player.change_chips(-bet)
                elif action[0] == CHECK:
                    has_action[self.turn] = False
                    pots[0] += action[1]
                elif action[0] == ALL_IN:
                    has_action[self.turn] = False
                    amount = action[1]
                    player.change_chips(-amount)
                    diff = amount - self.last_bet
            has_action[self.turn] = False
            

            self.turn = (self.turn + 1) % len(self.currently_playing)
            input()
        return

    def preflop(self, pots:list[int], players_in_pots):
        # setup
        for player in self.players:
            player.current_phase = ai_index.PRE_FLOP
        # blinds
        self.players[0].change_chips(self.small_blind)
        pots[0] += self.small_blind
        self.players[1].change_chips(self.big_blind)
        pots[0] += self.big_blind
        self.number_of_raises = 1
        self.to_call = self.big_blind
        self.last_bet = self.big_blind
        self.last_better = self.players[1]
        self.turn = 2
        if len(self.players) < 3:
            self.turn = 0
        # deal
        for player in self.currently_playing[0:]:
            player.hand.append(draw(self.deck))
            player.hand.append(draw(self.deck))

        # play
        return

    def allow_actions(self, actions):
        for i in range(len(actions)):
            actions[i] = True
        return

    def more_actions(self, has_action: list[bool]):
        for able in has_action:
            if able:
                return True
        return False

    def setup_players(self):
        for i in range(self.number_of_players):
            player = Ai()
            player.name = str(i)
            player.set_chip_base_amount(self.starting_chips)
            player.big_blind = self.big_blind
            for j in range(len(player.weights)):
                player.weights[j] = random.uniform(0.1, 2)
            print(f'player{i} set up')
            self.players.append(player)
        return


    def reset_globals(self):
        number_of_raises = 0
        to_call = 0
        last_bet = 0
        turn = 0
        return

if __name__ == '__main__':
    main()