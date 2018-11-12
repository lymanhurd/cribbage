from typing import List

Cards = List[int]

SUITS = ['C', 'D', 'H', 'S']
CARD_NAMES = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
DECK = [n + s for s in SUITS for n in CARD_NAMES]
PAIRS = (0, 0, 2, 6, 12)


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
    suit0 = hand[0] // 13
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


def score_cards(h: str, s: str, crib: bool = False) -> int:
    return score([card_number(c) for c in h.split(',')], card_number(s), crib)


def is_run(sub_seq: List[int]) -> bool:
    seq_len = len(sub_seq)
    val_seq = [s % 13 for s in sub_seq]
    if max(val_seq) - min(val_seq) != seq_len - 1:
        return False
    if len(set(val_seq)) != seq_len:
        return False
    return True


def score_card_seq(h: str) -> int:
    return score_sequence([card_number(c) for c in h.split(',')])


def score_sequence(seq: List[int]) -> int:
    points = 0
    # check for pair, pair royal, double pair royal
    cv = seq[-1]
    run = 1
    for s in reversed(seq[:-1]):
        if cv != s % 13:
            break
        else:
            run += 1
    points += PAIRS[run]
    if len(seq) >= 3:
        for i in range(min(len(seq), 8), 2, -1):
            if is_run(seq[-i:]):
                points += i
    count = sum(card_value(s) for s in seq)
    if count == 15 or count == 31:
        points += 2
    return points


if __name__ == '__main__':
    print(score_cards('2c,3c,4c,5c', '6d', False))
