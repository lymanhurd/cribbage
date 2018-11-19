"""Base Cribbage player using the most simple algorithm possible.  Given a hand it will always discard the first two
cards and it will always play the first card legally playable.
"""
from typing import List

import score


# noinspection PyUnusedLocal
class CribbagePlayer:
    def __init__(self):
        self.hand: List[int] = None
        self.computer_score = 0
        self.human_score = 0

    def discard_cards(self, human_score: int = 0, computer_score: int = 0) -> List[int]:
        """discard_cards chooses two cards to discard to crib"""
        assert len(self.hand) == 6
        discards = self.hand[:2]
        self.hand = self.hand[2:]
        return discards

    def new_hand(self, hand):
        """Restarts next hand and dealer status toggles."""
        assert len(hand) == 6
        self.hand = hand

    def play_card(self, seq: List[int], human_score: int = 0, computer_score: int = 0) -> int:
        """play_card chooses next card to play.  A return of -1 signifies saying Go"""
        assert 0 < len(self.hand) <= 4
        count = sum(score.card_value(s) for s in seq)
        idx_to_play = -1
        card_to_play = -1
        for i, h in enumerate(self.hand):
            if score.card_value(h) + count <= 31:
                idx_to_play = i
                break
        if idx_to_play != -1:
            card_to_play = self.hand[idx_to_play]
            del self.hand[idx_to_play]
        return card_to_play
