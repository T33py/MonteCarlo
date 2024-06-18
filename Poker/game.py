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
currently_playing: list[list[card.Card]] = []

def main():
    deck = make_deck()
    shuffle(deck)
    setup_players()


    return

def round():
    # setup
    hands = [common_cards, p.hand for p in players]
    currently_playing = [h for h in hands]

    # play
    preflop()

    # clean up
    empty_hands(hands, deck)
    shuffle(deck)
    
    # move button
    p = players.pop(0)
    players.append(p)
    return

def preflop():
    for hand in currently_playing[1:]:
        hand.append(draw(deck))
        hand.append(draw(deck))
    
    for i in range(len(players)):
        player = players[i]
        player.current_phase = ai_index.PRE_FLOP
    return

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