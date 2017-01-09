from Card import Card
from random import shuffle


class Deck:

    def __init__(self, is_pinochle=False):
        self.deck = []

        self.is_pinochle = is_pinochle  # we need to know if we're using a pinochle deck for later ordering
        # A pinochle deck may be formed by combining two normal decks of cards and removing cards 2-8, for a total of 48 cards.
        # In addition, pinochle uses unconventional card ordering, namely (from lowest to highest):  9, Jack, Queen, King, 10, Ace.
        if is_pinochle:
            ordered_values = list(Card.Values)
            ordered_values.sort(key=Deck.cmp_to_key(Deck.new_order_comparison))
            for suit in Card.Suits:
                for value in ordered_values:
                    if value.value not in range(2, 8 + 1):  # `range` is exclusive on the end value
                        self.deck.append(Card(suit=suit, value=value))
                        self.deck.append(Card(suit=suit, value=value))

        else:  # classic 52-card deck
            for suit in Card.Suits:
                for value in Card.Values:
                    self.deck.append(Card(suit=suit, value=value))

    # Randomizes the order of the cards.
    def shuffle(self):
        shuffle(self.deck)

    # Splits the deck at a point chosen by the player; cards above the split point are placed on the bottom of the deck
    # (without reordering). The first card below the split becomes the top of the deck.
    # The first card above the split becomes the bottom of the deck.
    def cut(self, split_point):
        if split_point < 0 or split_point >= len(self.deck):
            return
        self.deck = self.deck[split_point:] + split_point[:split_point]

    # Retrieves the top card and removes it from the deck.
    # throws index error if deck is empty
    def deal(self):
        return self.deck.pop(0)  # pop from the front, instead of the default last

    # Retrieves the top card but does not remove it from the deck.
    # throws index error if deck is empty
    def turn_over(self):
        return self.deck[0]

    # Finds the position of a given card in the deck (top of the deck is the first card, next card is the second, etc.).
    # returns -1 if card not found
    def search(self, other_card):
        for (index, card) in enumerate(self.deck):
            if card == other_card:
                return index
        return -1

    # Places the remaining cards in the deck in the order of a new deck of cards
    # (top to bottom: hearts A-K, clubs A-K, diamonds K-A, spades K-A).
    def new_order(self):
        self.deck.sort(key=Deck.cmp_to_key(Deck.new_order_comparison))

    # top to bottom: hearts A-K, clubs A-K, diamonds K-A, spades K-A)
    @staticmethod
    def new_order_comparison(card1, card2):
        # sort by suits first
        if card1.Suit.value != card2.Suit.value:
            return card1.Suit.value - card2.Suit.value
        # within the suits, sort hearts and clubs Ace->King [default]
        elif card1.Suit in [Card.Suits.HEARTS, Card.Suits.CLUBS]:
            return card1.Value.value - card2.Value.value
        # and sort diamonds and spades King->Ace [reversed]
        else:
            return -1 * (card1.Value.value - card2.Value.value)

    # pinochle uses unconventional card ordering, namely (from lowest to highest):  9, Jack, Queen, King, 10, Ace.
    @staticmethod
    def pinochle_order_comparison(card1, card2):
        # sort by suits first
        if card1.Suit.value != card2.Suit.value:
            return card1.Suit.value - card2.Suit.value
        else:
            value_ordering = [Card.Values.NINE, Card.Values.JACK, Card.Values.QUEEN, Card.Values.KING, Card.Values.TEN, Card.Values.ACE]
            return value_ordering.index(card1.Value) - value_ordering.index(card2.Value)

    def __str__(self):
        for card in self.deck:
            print(str(card))

    # Convert a cmp= function into a key= function
    @staticmethod
    def cmp_to_key(mycmp):
        class K(object):
            def __init__(self, obj, *args):
                self.obj = obj

            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0

            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0

            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0

            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0

            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0

            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
        return K