from Poker.pokerhands import make_deck, shuffle, draw, empty_hands, identify_hands, find_winners
from Poker.ai import Ai, BET, CALL, CHECK, FOLD, ALL_IN
import Poker.ai_index as ai_index
import Poker.card as card
import random

def main():
    game = PokerGame()
    game.setup_players()
    print(f'players {game.players}')
    redo = True
    while redo:
        game.play_round()

        if input('NEXT GAME\n') != '':
            redo = False

    return

class PokerGame:

    def __init__(self):
        # TODO: store and expose game stats - hands bets etc.
        self.number = 0
        self.verbose = True
        self.number_of_players = 8
        self.starting_chips: int = 1000
        self.big_blind: int = 10
        self.small_blind: int = 5

        self.deck: list[card.Card] = []
        self.players: list[Ai] = []
        self.common_cards: list[card.Card] = []
        self.hands: list[list[card.Card]] = []
        self.currently_playing: list[Ai] = []
        self.pot_contribution: list[int] = []

        self.number_of_raises: int = 0
        self.last_bet: int = 0
        self.last_better: Ai
        self.turn: int = 0
        self.deck = make_deck()
        shuffle(self.deck)

    def play_round(self):
        if self.verbose:
            print(f'game {self.number} starting round')
        # setup
        for player in self.players:
            player.big_blind = self.big_blind
            if player.chips < self.big_blind:
                player.chips += player.chip_base_amount
        self.hands = [p.hand for p in self.players]
        self.hands.insert(0, self.common_cards)
        self.currently_playing = [p for p in self.players]
        self.pot_contribution = [0 for p in self.players]
        # pot is in a list because i am lazy
        pots:list[int] = [ 0 ]
        players_in_pots = [self.currently_playing]
        # print(f'players at table {self.players}')
        # print(f'set up to play {self.currently_playing}')

        # play
        # print('PREFLOP')
        self.do_preflop(pots, players_in_pots)
        self.do_play(pots, players_in_pots)
        # print('FLOP')
        self.do_flop(pots, players_in_pots)
        self.do_play(pots, players_in_pots)
        # print('TURN')
        self.do_turn(pots, players_in_pots)
        self.do_play(pots, players_in_pots)
        # print('RIVER')
        self.do_river(pots, players_in_pots)
        self.do_play(pots, players_in_pots)

        self.print_state(pots)
        self.payout(pots, players_in_pots)

        # clean up
        empty_hands(self.hands, self.deck)
        shuffle(self.deck)
        self.number_of_raises = 0
        self.last_bet = 0
        self.turn = 0

        # move button
        p = self.players.pop(0)
        self.players.append(p)

        # reset players for next game
        for player in self.players:
            # print(f'player {player} ended with {player.chips} and a win/loss of {player.chip_win_loss}')
            player.reset()
        return

    def print_state(self, pots):
        if self.verbose:
            print(f'hands: {self.compile_hands(self.currently_playing)}\n bets: {self.pot_contribution}\n pots: {pots}')
        return

    def do_play(self, pots:list[int], players_in_pots: list[list[Ai]]):
        # print(f'playing with {self.currently_playing}')
        has_action = [True for player in self.currently_playing]
        checks = 0
        while self.more_actions(has_action) and len(self.currently_playing) > 1:
            player = self.currently_playing[self.turn]
            # figure out if anyone needs to do something
            self.allow_actions(has_action)
            for i in range(len(self.currently_playing)):
                if self.currently_playing[i].chips <= 0 or self.currently_playing[i].is_all_in:
                    has_action[i] = False
            if has_action[self.turn]:
                if self.verbose:
                    print(f'its {player.name}s ({player.chips}) turn')
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
                    checks = 0
                elif action[0] == CALL:
                    has_action[self.turn] = False
                    bet = action[1]
                    pots[0] += bet
                    player.change_chips(-bet)
                    self.pot_contribution[self.turn] += bet
                    checks += 1
                elif action[0] == CHECK:
                    has_action[self.turn] = False
                    checks += 1
                elif action[0] == ALL_IN:
                    has_action[self.turn] = False
                    amount = action[1]
                    player.change_chips(-amount)
                    self.pot_contribution[self.turn] += amount
                    diff = max(self.pot_contribution) - amount
                    if diff < 0: # if the player raised with the all in
                        self.number_of_raises += 1
                        diff *= -1
                        self.allow_actions(has_action)
                        checks = 0
                    else:
                        checks += 1
                    player.is_all_in = True
                    player.is_all_in_for = pots[0] + amount
                    pots[0] += amount
                    for _p in self.currently_playing:
                        if _p.is_all_in:
                            if amount > _p.is_all_in_with:
                                _p.is_all_in_for += _p.is_all_in_with
                            else:
                                _p.is_all_in_for += amount

            if self.verbose:
                self.print_state(pots)
                print(f'has action: {has_action}, turn: {self.turn}')

            if checks == len(self.currently_playing):
                break
            
            self.turn = (self.turn + 1) % len(self.currently_playing)
            # input()
        for player in self.currently_playing:
            if player.is_all_in:
                player.is_all_in_with = 0
        return

    def do_preflop(self, pots:list[int], players_in_pots):
        self.print_state(pots)
        # setup
        for player in self.players:
            player.current_phase = ai_index.PRE_FLOP
        # blinds
        self.players[0].change_chips(-self.small_blind)
        pots[0] += self.small_blind
        self.pot_contribution[0] += self.small_blind
        self.players[1].change_chips(-self.big_blind)
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
    
    def do_flop(self, pots:list[int], players_in_pots: list[list[Ai]]):
        self.print_state(pots)
        # setup
        for player in self.players:
            player.current_phase = ai_index.FLOP
        for i in range(len(self.pot_contribution)):
            self.pot_contribution[i] = 0
        self.common_cards.append(draw(self.deck))
        self.common_cards.append(draw(self.deck))
        self.common_cards.append(draw(self.deck))
        return

    def do_turn(self, pots:list[int], players_in_pots: list[list[Ai]]):
        self.print_state(pots)
        # setup
        for player in self.players:
            player.current_phase = ai_index.TURN
        for i in range(len(self.pot_contribution)):
            self.pot_contribution[i] = 0
        self.common_cards.append(draw(self.deck))
        return

    def do_river(self, pots:list[int], players_in_pots: list[list[Ai]]):
        self.print_state(pots)
        # setup
        for player in self.players:
            player.current_phase = ai_index.RIVER
        for i in range(len(self.pot_contribution)):
            self.pot_contribution[i] = 0
        self.common_cards.append(draw(self.deck))
        return
    
    def payout(self, pots:list[int], players_in_pots: list[list[Ai]]):
        if self.verbose:
            print(f'paying out {pots}, {players_in_pots}')

        for i in range(len(pots)):
            pot = pots[i]
            players = players_in_pots[i]
            hands = self.compile_hands(players)
            results = identify_hands(hands)
            winners = find_winners(results)
            for _winner in winners:
                winner: Ai = players[results.index(_winner)]
                max_win = int(pots[i] / len(winners))
                if winner.is_all_in and max_win > winner.is_all_in_for and len(winners) > 1:
                    max_win = winner.is_all_in_for / len(winners)
                winner.change_chips(max_win)
                pot -= max_win
                if self.verbose:
                    print(f'{max_win} from pot {i} ({pots[i]} -> {pot}) goes to {winner} because {hands} -> {winners}')
                
            if pot > 0: # handle rounding errors by giving the top hand any extra chips
                winner: Ai = players[results.index(winners[0])]
                winner.change_chips(pot)
                
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
        if self.verbose:
            print(f'game {self.number} setting up {self.number_of_players} new AIs')
        for i in range(self.number_of_players):
            player = Ai()
            player.name = str(i)
            player.set_chip_base_amount(self.starting_chips)
            player.big_blind = self.big_blind
            for j in range(len(player.weights)):
                player.weights[j] = random.uniform(0.1, 1.1)
            # print(f'player{i} set up')
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