from Poker.pokerhands import make_deck, shuffle, draw, empty_hands, identify_hands, find_winners
from Poker.ai import Ai
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
    pot:int = 0

    # play
    pot += preflop(pot)

    # clean up
    empty_hands(hands, deck)
    shuffle(deck)

    # move button
    p = players.pop(0)
    players.append(p)
    return

def preflop(pot:int):
    # setup
    has_action = []
    for player in players:
        player.current_phase = ai_index.PRE_FLOP
        has_action.append(True)
    turn = 2
    if len(players) < 3:
        turn = 0
    to_call = 0
    number_of_raises = 1
    # blinds
    players[0].change_chips(small_blind)
    pot += small_blind
    players[1].change_chips(big_blind)
    pot += big_blind
    to_call = big_blind
    # deal
    for player in currently_playing[1:]:
        player.hand.append(draw(deck))
        player.hand.append(draw(deck))

    # play
    while check_done(has_action):
        player = currently_playing[turn]
        action = player.take_action(hands[0], pot, to_call, len(currently_playing), turn, number_of_raises)
        has_action[turn] = False
        turn = (turn + 1) % len(currently_playing)

    return pot

def check_done(has_action: list[bool]):
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


if __name__ == '__main__':
    main()