from enum import Enum


class Hand(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def create_from_str(cls, s1, s2):
        lookup = {
            'A': cls.ROCK,
            'B': cls.PAPER,
            'C': cls.SCISSORS,
        }
        opponent_hand = lookup[s1]
        lookup = {
            'X': opponent_hand.lose,
            'Y': opponent_hand,
            'Z': opponent_hand.win,
        }
        my_hand = lookup[s2]
        return opponent_hand, my_hand

    def __gt__(self, other):
        if self == Hand.ROCK and other == Hand.SCISSORS:
            return True
        elif self == Hand.PAPER and other == Hand.ROCK:
            return True
        elif self == Hand.SCISSORS and other == Hand.PAPER:
            return True

    @property
    def win(self):
        if self == Hand.ROCK:
            return Hand.PAPER
        elif self == Hand.PAPER:
            return Hand.SCISSORS
        elif self == Hand.SCISSORS:
            return Hand.ROCK

    @property
    def lose(self):
        if self == Hand.ROCK:
            return Hand.SCISSORS
        elif self == Hand.PAPER:
            return Hand.ROCK
        elif self == Hand.SCISSORS:
            return Hand.PAPER


opponent_score = 0
my_score = 0

with open('input.txt', 'r') as f:
    for row in f:
        hands = row.strip('\n').split(' ')
        opponent_hand, my_hand = Hand.create_from_str(*hands)
        opponent_score += opponent_hand.value
        my_score += my_hand.value
        if opponent_hand == my_hand:
            opponent_score += 3
            my_score += 3
        elif opponent_hand > my_hand:
            opponent_score += 6
        else:
            my_score += 6

print(f'My score: {my_score}\nOpponent score: {opponent_score}')
