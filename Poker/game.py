from Poker.pokerhands import make_deck, shuffle, draw, empty_hands, identify_hands, find_winners
from Poker.ai import Ai, BET, CALL, CHECK, FOLD, ALL_IN
import Poker.ai_index as ai_index
import Poker.card as card

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

def main():
    deck = make_deck()
    shuffle(deck)
    setup_players()

    play_round()


    return

def play_round():
    # setup
    hands = [common_cards, p.hand for p in players]
    currently_playing = [p for p in players]
    pots:list[int] = [ 0 ]
    players_in_pots = [currently_playing]

    # play
    preflop(pots)
    do_play(pots, players_in_pots)

    # clean up
    empty_hands(hands, deck)
    shuffle(deck)

    # move button
    p = players.pop(0)
    players.append(p)

    # rebuy
    for player in players:
        if player.chips == 0:
            player.chips += player.chip_base_amount
    return

def do_play(pots:list[int], players_in_pots):
    has_action = [True for player in currently_playing]
    while more_actions(has_action):
        player = currently_playing[turn]
        action = player.take_action(hands[0], sum(pots), to_call, len(currently_playing), turn, number_of_raises)
        has_action[turn] = False
        if action[0] == FOLD:
            currently_playing.pop(turn)
            has_action.pop(turn)
        elif action[0] == BET:
            allow_actions(has_action)
            has_action[turn] = False
            bet = action[1]
            player.change_chips(-bet)
            pots[0] += bet
            diff = bet - last_bet
            to_call += diff
            last_bet = diff
            last_better = player
            number_of_raises += 1
        elif action[0] == CALL:
            has_action[turn] = False
            pots[0] += action[1]
            player.change_chips(-bet)
        elif action[0] == CHECK:
            has_action[turn] = False
            pots[0] += action[1]
        elif action[0] == ALL_IN:
            has_action[turn] = False
            amount = action[1]
            player.change_chips(-amount)
            diff = amount - last_bet
            

        turn = (turn + 1) % len(currently_playing)
    return

def preflop(pots:list[int], players_in_pots):
    # setup
    for player in players:
        player.current_phase = ai_index.PRE_FLOP
    # blinds
    players[0].change_chips(small_blind)
    pots[0] += small_blind
    players[1].change_chips(big_blind)
    pots[0] += big_blind
    number_of_raises = 1
    to_call = big_blind
    last_bet = big_blind
    last_better = players[1]
    turn = 2
    if len(players) < 3:
        turn = 0
    # deal
    for player in currently_playing[1:]:
        player.hand.append(draw(deck))
        player.hand.append(draw(deck))

    # play
    return

def allow_actions(actions):
    for i in range(len(actions)):
        actions[i] = True
    return

def more_actions(has_action: list[bool]):
    for able in has_action:
        if able:
            return True
    return False

def setup_players():
    for i in range(number_of_players):
        player = Ai()
        player.name = str(i)
        player.set_chip_base_amount(starting_chips)
        player.current_big_blind = big_blind
        players.append(player)
    return


def reset_globals():
    number_of_raises = 0
    to_call = 0
    last_bet = 0
    turn = 0
    return
if __name__ == '__main__':
    main()