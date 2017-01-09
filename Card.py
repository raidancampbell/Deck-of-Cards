from enum import Enum, unique


class Card:
    @unique
    class Suits(Enum):
        HEARTS = 1
        CLUBS = 2
        DIAMONDS = 3
        SPADES = 4

    @unique
    class Values(Enum):
        ACE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6
        SEVEN = 7
        EIGHT = 8
        NINE = 9
        TEN = 10
        JACK = 11
        QUEEN = 12
        KING = 13

    def __init__(self, suit, value):
        self.Suit = suit
        self.Value = value

    # equality compares both suit and value
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.Suit == other.Suit and self.Value == other.Value
        else:
            return False

    # less than / greater than compare only by value
    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.Value.value < other.Value.value
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.Value.value > other.Value.value
        else:
            return False

    def __str__(self):
        return self.Value.name.lower() + ' of ' + self.Suit.name.lower()
