from typing import List

Cards = List[int]

SUITS = ['C', 'D', 'H', 'S']
CARD_NAMES = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
DECK = [n + s for s in SUITS for n in CARD_NAMES]


def card_number(name: str) -> int:
    return DECK.index(name.upper())


def card_value(card: int) -> int:
    return min(10, 1 + card % 13)


def ways_to_make_sum(n: int, l: List[int]) -> int:
    if n <= 0 or len(l) == 0:
        return 0
    if l[0] == n:
        return 1 + ways_to_make_sum(n, l[1:])
    else:
        return ways_to_make_sum(n - l[0], l[1:]) + ways_to_make_sum(n, l[1:])


def score(hand: Cards, start: int, is_crib: bool) -> int:
    points = 0
    # nibs
    start_suit = start // 13
    for h in hand:
        if start_suit == h // 13 and h % 13 == 10:
            points += 1
    suit0 = hand[0] / 13
    # flush
    flush = True
    for h in hand[1:]:
        if h // 13 != suit0:
            flush = False
            break
    if flush:
        if suit0 == start_suit:
            points += 5
        elif not is_crib:
            points += 4
    # all subsequent clauses do not distinguish starter card form hand cards
    hand.append(start)
    # pairs, pair royals, double pair royal
    PAIRS = (0, 0, 2, 6, 12)
    hist = 13 * [0]
    for h in hand:
        hist[h % 13] += 1
    run = 0
    product = 1
    for n in hist:
        points += PAIRS[n]
        # a zero means a run is broken
        if n == 0:
            if run >= 3:
                points += run * product
                run = 0
                product = 1
        else:
            product *= n
            run += 1
    # 15's
    points += 2 * ways_to_make_sum(15, [card_value(h) for h in hand])
    return points


def score_cards(h: str, s: str) -> int:
    return score([card_number(c) for c in h.split(',')], card_number(s), False)


if __name__ == '__main__':
    print(score_cards('2c,3c,4h,9d', '6c'))
