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
    verbose = True
    number_of_players = 5
    starting_chips: int = 1000
    big_blind: int = 10
    small_blind: int = 5

    deck: list[card.Card] = []
    players: list[Ai] = []
    common_cards: list[card.Card] = []
    hands: list[list[card.Card]] = []
    currently_playing: list[Ai] = []
    pot_contribution: list[int] = []

    number_of_raises: int = 0
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
        self.pot_contribution = [0 for p in self.players]
        pots:list[int] = [ 0 ]
        players_in_pots = [self.currently_playing]
        print(f'players at table {self.players}')
        print(f'set up to play {self.currently_playing}')

        # play
        print('preflop setup')
        self.preflop(pots, players_in_pots)
        print('preflop play')
        self.do_play(pots, players_in_pots)

        self.payout(pots, players_in_pots)

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

    def do_play(self, pots:list[int], players_in_pots: list[list[Ai]]):
        print(f'playing with {self.currently_playing}')
        has_action = [True for player in self.currently_playing]
        while self.more_actions(has_action):
            player = self.currently_playing[self.turn]
            if player.chips > 0:
                if self.verbose:
                    print(f'its {player.name}s turn')
                action = player.take_action(
                    common_cards=self.hands[0], 
                    pot=sum(pots), 
                    to_call=max(self.pot_contribution) - self.pot_contribution[self.turn], 
                    players=len(self.currently_playing), 
                    pos=self.turn, 
                    raises=self.number_of_raises, 
                    verbose=self.verbose
                    )
                if action[0] == FOLD:
                    self.currently_playing.pop(self.turn)
                    self.pot_contribution.pop(self.turn)
                    has_action.pop(self.turn)
                    self.turn -= 1
                elif action[0] == BET:
                    self.allow_actions(has_action)
                    has_action[self.turn] = False
                    bet = action[1]
                    player.change_chips(-bet)
                    pots[0] += bet
                    self.pot_contribution[self.turn] += bet
                    diff = bet - self.last_bet
                    self.last_bet = diff
                    self.last_better = player
                    self.number_of_raises += 1
                elif action[0] == CALL:
                    has_action[self.turn] = False
                    bet = action[1]
                    pots[0] += bet
                    player.change_chips(-bet)
                    self.pot_contribution[self.turn] += bet
                elif action[0] == CHECK:
                    has_action[self.turn] = False
                elif action[0] == ALL_IN:
                    has_action[self.turn] = False
                    amount = action[1]
                    player.change_chips(-amount)
                    diff = max(self.pot_contribution) - amount
                    if diff < 0: # if the player raised with the all in
                        self.number_of_raises += 1
                        diff *= -1
                    pots[0] -= diff
                    pots.insert(0, diff)
                    players_not_allin = players_in_pots[0].copy()
                    players_not_allin.remove(player)
                    players_in_pots.insert(0, players_not_allin)
                    self.currently_playing = players_not_allin
                    
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
        self.pot_contribution[0] += self.small_blind
        self.players[1].change_chips(self.big_blind)
        pots[0] += self.big_blind
        self.pot_contribution[1] += self.big_blind
        self.number_of_raises = 1
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
    
    def payout(self, pots:list[int], players_in_pots: list[list[Ai]]):
        if self.verbose:
            print(f'paying out {pots}, {players_in_pots}')
        for i in range(len(pots)):
            players = players_in_pots[i]
            hands = self.compile_hands(players)
            results = identify_hands(hands)
            winners = find_winners(results)
            for _winner in winners:
                winner: Ai = players[results.index(_winner)]
                winner.change_chips(int(pots[i] / len(winners)))
                if self.verbose:
                    print(f'pot {i} ({pots[i]}) goes to {winner} because {hands} -> {winners}')


        return
    
    def compile_hands(self, players):
        hnds = []
        hnds.append(self.common_cards)
        for player in players:
            hnds.append(player.hand)
        return hnds

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
                player.weights[j] = random.uniform(0.1, 1.1)
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