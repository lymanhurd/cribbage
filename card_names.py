from typing import List
import score

"""Some convenience methods for referring to cards by their ASCII names (case insensitive)."""

SUITS = ['C', 'D', 'H', 'S']
CARD_NAMES = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
DECK = [n + s for s in SUITS for n in CARD_NAMES]


def score_cards(h: str, s: str, crib: bool = False) -> int:
    """score_cards adds up the points for a four-card hand represented as a comma-separated string
    and a single start card.  The crib Boolean value only affects if flushes of four cards, i.e.,
    the hand has all one suit and the started card is another, counts for 4 points (yes for hand,
    no for crib)
    """
    return score.score([_card_number(c) for c in h.split(',')], _card_number(s), crib)


def score_card_seq(h: str) -> int:
    """score_card_seq gives the incremental core from adding a new card to an existing sequence of
    cards. It does not check that the play is legal and it does not add a point for an opponent's
    "go" short of 31 as it does not have this information.
    """
    return score.score_sequence([_card_number(c) for c in h.split(',')])


def card_names(cards: List[int]) -> str:
    return ' '.join([DECK[c] for c in cards])


def _card_number(name: str) -> int:
    return DECK.index(name.upper())


if __name__ == '__main__':
    # print(score_cards('2c,3c,4c,5c', '6d', False))
    print(score_cards('5c,2h,10d,2c', 'ks', False))
