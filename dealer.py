from typing import List

import hashlib
import secrets


class CribbageError(Exception):
    """Base class for exceptions in this module."""
    pass


class Deal:
    def __init__(self):
        # Perform initial shuffle.  The first 13 cards will later be shuffled by the human too.
        self.deck: List[int] = list(range(52))
        for i in range(51, 0, -1):
            t = self.deck[i]
            n = secrets.randbelow(i)
            self.deck[i] = self.deck[n]
            self.deck[n] = t
        # Keep track of state.  Start --> Committed --> Seeded --> Completed
        self.committed: bool = False
        self.seeded: bool = False
        self.completed = False

    # This method proves that the computer has not tampered with the deck in response to the human seeding.
    def commit_deal(self) -> str:
        deck_string = ''.join(['{:02}'.format(c) for c in self.deck])
        h = hashlib.sha3_256()
        h.update(deck_string.encode())
        self.committed = True
        return h.hexdigest()

    # The human has the option of further shuffling the first 13 cards (6 for each hand plus one to determine dealer).
    def human_hand(self, seed: List[int] = None) -> List[int]:
        if not self.committed:
            raise CribbageError('Must call commit_deal() first.')
        if seed:
            if len(set(seed)) != 13:
                raise CribbageError('Invalid seed {}.'.format(seed))
            if min(seed) < 0 or max(seed) > 51:
                raise CribbageError('Invalid seed {}.'.format(seed))
            for i in range(13):
                self.deck[i] = (self.deck[i] + seed[i]) % 52
        self.seeded = True
        return self.deck[:6]

    # This is only called by the computer, in fact it is the only method called by the computer player.
    def computer_hand(self) -> List[int]:
        if not self.seeded:
            raise CribbageError('Must call human_hand() first.')
        return self.deck[6:12]

    # The traditional cut for deal has the problem of ties.  Therefore we use an equivalent method.
    def human_is_dealer(self) -> bool:
        if not self.seeded:
            raise CribbageError('Must call human_hand() first.')
        return self.deck[12] % 2 == 0

    # Once all the cards have been revealed, the human can verify the entire initial deal.
    def mark_hand_completed(self):
        self.completed = True

    def verify_deck(self) -> List[int]:
        if not self.completed:
            raise CribbageError('The computer must call mark_hand_completed() first.')
        return self.deck


if __name__ == "__main__":
    d = Deal()
    print(d.deck)
    print(d.commit_deal())
    print(d.human_hand(list(range(13))))
    print(d.computer_hand())
    print(d.human_is_dealer())
    d.mark_hand_completed()
    print(d.verify_deck())
