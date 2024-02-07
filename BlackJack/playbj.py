from BlackJack.black_jack import black_jack

bj = black_jack()
games = 10000000

stop_val_from = 17
stop_val_to = 17

double_values = [7,8,9,10]

assume_double_value_from = 7
assume_double_value_to = 10

assume_dealer_has_from = 8
assume_dealer_has_to = 9

results = {}


def main():
# make this a 6 deck game
    for i in range(5):
        bj.deck.extend(bj.template_deck)
    bj.shuffle(bj.deck)

    for sv in range(stop_val_from, stop_val_to+1):
        for adh in range(assume_dealer_has_from, assume_dealer_has_to+1):
            for adv in range(assume_double_value_from, assume_double_value_to+1):
                for dvs in range(len(double_values)):
                    for dve in range(len(double_values)-dvs):
                        dv = double_values[dvs:dvs+dve]
                        results[run_hands(sv, adh, dv, adv)] = [sv, adh, dv, adv]

    print(results)
    scores = list(results.keys())
    scores.sort()
    scores.reverse()
    for i in range(20):
        score = scores[i]
        stop_val = results[score][0]
        assume_dealer_has = results[score][1]
        doubles = results[score][2]
        assume_double_value = results[score][3]
        print(f'sv: {stop_val}, adv {assume_double_value}, dv: {doubles}, adh: {assume_dealer_has}, score: {score} => {(score/games)*100:.2f}%')


# print(bj.template_deck)
# print(bj.deck)

def run_hands(stop_val, assume_dealer_has, doubles, assume_double_value):
    score = 0
    for i in range(games):
        score += play(stop_val, assume_dealer_has, doubles, assume_double_value)
    print(f'sv: {stop_val}, adv {assume_double_value}, dv: {doubles}, adh: {assume_dealer_has}, score: {score} => {(score/games)*100:.2f}%')
    return score


def should_hit(hand, dealers_card, stop_val, assume_dealer_has):
    hs = bj.hand_value(hand)
    ds = bj.hand_value([dealers_card])
    # the value at which we allways stop
    if hs >= stop_val:
        return False
    # if we have a value higher than the assumption about the dealers hidden card
    if hs > ds + assume_dealer_has:
        return False
    
    return True

def should_double_down(hand, dealers_card, doubles, assume_double_value, assume_dealer_has):
    if len(hand) > 2:
        return False
    hs = bj.hand_value(hand)
    ds = bj.hand_value([dealers_card])

    if hs in doubles and hs + assume_double_value > ds + assume_dealer_has:
        return True
    
    return False

def play(stop_val, assume_dealer_has, doubles, assume_double_value):
    bj.deal(1, [1])
    hand = bj.hands[0]
    dealer_shows = bj.dealers_hand[0]
    multiplier = 1
    while should_hit(hand, dealer_shows, stop_val, assume_dealer_has):
        bj.hit(hand)
        if should_double_down(hand, dealer_shows, doubles, assume_double_value, assume_dealer_has):
            multiplier = 2
            break
    bj.play_dealer()

    return bj.winner(hand) * multiplier



if __name__ == '__main__':
    main()

