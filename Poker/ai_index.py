# indexes in the list of weights for the ai


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
NUMBER_OF_PARAMETERS = 100
PARAMETERS: int = 4*52*52


POT_SIZE_VALUE: int = PARAMETERS+0
NUMBER_OF_RAISES_MODIFIER: int = PARAMETERS+1
NUMBER_OF_RAISES_MULTIPLIER: int = PARAMETERS+2
NEEDED_TO_CALL_MODIFIER: int = PARAMETERS+3

REMAINING_CHIPCOUNT_VALUE: int = PARAMETERS+10
REMAINING_CHIPCOUNT_THRESHOLD: int = PARAMETERS+11
REMAINING_CHIPCOUNT_TO_BIGBLIND_CUTOFF: int = PARAMETERS+12
CHECK_CUTOFF: int = PARAMETERS+13
CALL_CUTOFF: int = PARAMETERS+14

POSITION_MODIFIER: int = PARAMETERS+20
NUMBER_OF_OTHER_PLAYERS_MODIFIER: int = PARAMETERS+21
