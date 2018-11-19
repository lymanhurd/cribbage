from dealer import Deal
from player import CribbagePlayer
from score import score
from card_names import card_names


class CribbageGame:
    def __init__(self, p1: CribbagePlayer, p2: CribbagePlayer):
        self.p1: CribbagePlayer = p1
        self.p2: CribbagePlayer = p2
        self.p1_score: int = 0
        self.p2_score: int = 0

    def play_game(self):
        hand_num = 1
        d = Deal()
        d.commit_deal()  # ignoring return for now
        self.p1.new_hand(d.human_hand())
        self.p2.new_hand(d.computer_hand())
        start = d.start_card()
        p1_deals = d.human_is_dealer()
        while max(self.p1_score, self.p2_score) < 121:
            print("Hand # {} Starting new hand p1 score = {} p2 score = {}".format(hand_num, self.p1_score,
                                                                                   self.p2_score))
            hand_num += 1
            if p1_deals:
                print("Player 1 deals")
            else:
                print("Player 2 deals")
            crib = self.p1.discard_cards() + self.p2.discard_cards()
            crib_score = score(crib, start, is_crib=True)
            hand1_score = score(self.p1.hand, start)
            hand2_score = score(self.p2.hand, start)
            print("Start {}\nP1 hand {} score {}\nP2 hand {} score {}\ncrib    {} score {}.\n".format(card_names(
                [start]), card_names(self.p1.hand), hand1_score, card_names(self.p2.hand), hand2_score,
                card_names(crib), crib_score))
            if p1_deals:
                self.p2_score += hand2_score
                if self.p2_score > 120:
                    print("P2 wins.  Final score: {}-{}\n".format(self.p1_score, self.p2_score))
                    break
                self.p1_score += hand1_score + crib_score
                if self.p1_score > 120:
                    print("P1 wins.  Final score: {}-{}\n".format(self.p1_score, self.p2_score))
                    break
            else:
                self.p1_score += hand1_score
                if self.p1_score > 120:
                    print("P1 wins.  Final score: {}-{}\n".format(self.p1_score, self.p2_score))
                    break
                self.p2_score += hand2_score + crib_score
                if self.p2_score > 120:
                    print("P2 wins.  Final score: {}-{}\n".format(self.p1_score, self.p2_score))
                    break
            d = Deal()
            d.commit_deal()  # ignoring return for now
            self.p1.new_hand(d.human_hand())
            self.p2.new_hand(d.computer_hand())
            start = d.start_card()
            p1_deals = not p1_deals


def main():
    p1 = CribbagePlayer()
    p2 = CribbagePlayer()
    game = CribbageGame(p1, p2)
    game.play_game()


if __name__ == '__main__':
    main()
