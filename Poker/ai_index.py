# indexes in the list of weights for the ai
NUMBER_OF_PARAMETERS = 16


# cards are sorted by suit
HEARTS: int   = 0
DIAMONDS: int = 13
SPADES: int   = 26
KLUBS: int    = 39
suits_index = {
    'H': HEARTS,
    'D': DIAMONDS,
    'S': SPADES,
    'K': KLUBS
}

# weights for each card relative to each other card for each phase start at these indexes
PRE_FLOP: int = 0
FLOP: int     = 52*52
TURN: int     = 2*52*52
RIVER: int    = 3*52*52

# parameter weights start after all of the cards
PARAMETERS: int = 4*52*52
RAISE_PREFLOP: int = PARAMETERS+0
RAISE_FLOP: int = PARAMETERS+1
RAISE_TURN: int = PARAMETERS+2
RAISE_RIVER: int = PARAMETERS+3
CALL_PREFLOP: int = PARAMETERS+4
CALL_FLOP: int = PARAMETERS+5
CALL_TURN: int = PARAMETERS+6
CALL_RIVER: int = PARAMETERS+7
FOLD_PREFLOP: int = PARAMETERS+8
FOLD_FLOP: int = PARAMETERS+9
FOLD_TURN: int = PARAMETERS+10
FOLD_RIVER: int = PARAMETERS+11
ALL_IN_PREFLOP: int = PARAMETERS+12
ALL_IN_FLOP: int = PARAMETERS+13
ALL_IN_TURN: int = PARAMETERS+14
ALL_IN_RIVER: int = PARAMETERS+15