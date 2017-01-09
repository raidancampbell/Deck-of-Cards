from unittest import TestCase
from Deck import Deck
from Card import Card
import random


class Tests(TestCase):
    def setUp(self):
        random.seed(a=42)  # seed `random` with a constant to provide deterministic testing
        self.card = Card(suit=Card.Suits.SPADES, value=Card.Values.ACE)
        self.deck = Deck()
        self.pinochle = Deck(is_pinochle=True)

    def test_card_constructor(self):
        card = Card(suit=Card.Suits.SPADES, value=Card.Values.ACE)
        self.assertEqual(card.Suit, Card.Suits.SPADES)
        self.assertEqual(card.Value, Card.Values.ACE)

    def test_card_equality(self):
        original_card = Card(suit=Card.Suits.SPADES, value=Card.Values.ACE)
        different_suit = Card(suit=Card.Suits.HEARTS, value=Card.Values.ACE)
        different_value = Card(suit=Card.Suits.SPADES, value=Card.Values.KING)
        different_both = Card(suit=Card.Suits.CLUBS, value=Card.Values.JACK)
        duplicate_card = Card(suit=Card.Suits.SPADES, value=Card.Values.ACE)
        self.assertNotEqual(original_card, different_suit)
        self.assertNotEqual(original_card, different_value)
        self.assertNotEqual(original_card, different_both)
        self.assertEqual(original_card, duplicate_card)

    def test_card_hash(self):
        original_card = Card(suit=Card.Suits.SPADES, value=Card.Values.ACE)
        different_suit = Card(suit=Card.Suits.HEARTS, value=Card.Values.ACE)
        different_value = Card(suit=Card.Suits.SPADES, value=Card.Values.KING)
        different_both = Card(suit=Card.Suits.CLUBS, value=Card.Values.JACK)
        duplicate_card = Card(suit=Card.Suits.SPADES, value=Card.Values.ACE)
        self.assertNotEqual(hash(original_card), hash(different_suit))
        self.assertNotEqual(hash(original_card), hash(different_value))
        self.assertNotEqual(hash(original_card), hash(different_both))
        self.assertEqual(hash(original_card), hash(duplicate_card))

    def test_card_comparison(self):
        original_card = Card(suit=Card.Suits.SPADES, value=Card.Values.ACE)
        different_value = Card(suit=Card.Suits.SPADES, value=Card.Values.KING)
        duplicate_card = Card(suit=Card.Suits.SPADES, value=Card.Values.ACE)
        self.assertTrue(original_card < different_value)
        self.assertFalse(original_card < duplicate_card or original_card > duplicate_card)

    def test_deck_constructor(self):
        # does default have 52 cards?
        self.assertEqual(len(self.deck.deck), 52)
        # does pinochle have 48 cards?
        self.assertEqual(len(self.pinochle.deck), 48)

        # does default have any duplicate cards?
        self.assertEqual(len(self.deck.deck), len(set(self.deck.deck)))
        # does pinochle have any duplicate cards? (more than expected)
        self.assertEqual(len(self.pinochle.deck), len(set(self.pinochle.deck)) * 2)

        # should also test the ordering of both decks

    def test_deck_shuffle(self):
        shuffled = self.deck
        # first card is the ace of hearts
        self.assertTrue(shuffled.turn_over(), Card(Card.Suits.HEARTS, Card.Values.ACE))

        # shuffle
        shuffled.shuffle()
        # first card should be different now.  `random` was seeded to provide deterministic results
        self.assertTrue(shuffled.turn_over(), Card(Card.Suits.HEARTS, Card.Values.TEN))

        # make sure nothing unexpected happened (i.e. we still have 52 cards, and no duplicates
        self.assertEqual(len(shuffled.deck), 52)
        self.assertEqual(len(shuffled.deck), len(set(shuffled.deck)))

    def test_deck_cut(self):
        self.assertRaises(IndexError, self.deck.cut(-1))
        self.assertRaises(IndexError, self.deck.cut(500))

        self.assertEqual(self.deck.deck[0], Card(Card.Suits.HEARTS, Card.Values.ACE))
        self.assertEqual(self.deck.deck[1], Card(Card.Suits.HEARTS, Card.Values.TWO))
        self.assertEqual(self.deck.deck[30], Card(Card.Suits.DIAMONDS, Card.Values.FIVE))
        self.assertEqual(self.deck.deck[31], Card(Card.Suits.DIAMONDS, Card.Values.SIX))
        self.assertEqual(self.deck.deck[32], Card(Card.Suits.DIAMONDS, Card.Values.SEVEN))
        self.assertEqual(self.deck.deck[33], Card(Card.Suits.DIAMONDS, Card.Values.EIGHT))
        self.assertEqual(self.deck.deck[50], Card(Card.Suits.SPADES, Card.Values.QUEEN))
        self.assertEqual(self.deck.deck[51], Card(Card.Suits.SPADES, Card.Values.KING))

        self.deck.cut(32)

        self.assertEqual(self.deck.deck[0], Card(Card.Suits.DIAMONDS, Card.Values.SEVEN))
        self.assertEqual(self.deck.deck[1], Card(Card.Suits.DIAMONDS, Card.Values.EIGHT))

        # these are not equal, because the virtual split point has now changed, and the bisection is at 19
        self.assertNotEqual(self.deck.deck[30], Card(Card.Suits.HEARTS, Card.Values.ACE))
        self.assertNotEqual(self.deck.deck[31], Card(Card.Suits.HEARTS, Card.Values.TWO))
        self.assertNotEqual(self.deck.deck[32], Card(Card.Suits.SPADES, Card.Values.QUEEN))
        self.assertNotEqual(self.deck.deck[33], Card(Card.Suits.SPADES, Card.Values.KING))

        self.assertEqual(self.deck.deck[50], Card(Card.Suits.DIAMONDS, Card.Values.FIVE))
        self.assertEqual(self.deck.deck[51], Card(Card.Suits.DIAMONDS, Card.Values.SIX))

    def test_deck_deal(self):
        card_on_top = self.deck.turn_over()
        self.assertEqual(len(self.deck.deck), 52)

        dealt_card = self.deck.deal()

        self.assertEqual(card_on_top, dealt_card)
        self.assertEqual(len(self.deck.deck), 51)
        self.assertTrue(dealt_card not in self.deck.deck)
        self.assertNotEqual(card_on_top, self.deck.turn_over())

        # deal the remaining cards
        for card_num in range(51):
            self.deck.deal()
        # expect an exception if there's no cards left
        self.assertRaises(IndexError, self.deck.deal)

    def test_deck_turn_over(self):
        self.assertEqual(self.deck.turn_over(), self.deck.deck[0])
        self.deck.deal()
        self.assertEqual(self.deck.turn_over(), self.deck.deck[0])
        next_card = self.deck.deck[1]
        self.deck.deal()
        self.assertEqual(self.deck.turn_over(), next_card)

        # deal the remaining cards
        for _ in range(50):
            self.deck.deal()

        # expect an exception if there's no cards left
        self.assertRaises(IndexError, self.deck.turn_over)

    def test_deck_search(self):
        self.assertEqual(self.deck.search(self.card), self.deck.deck.index(self.card))
        top_card = self.deck.deal()
        self.assertEqual(self.deck.search(top_card), -1)

        # deal the remaining cards out
        for _ in range(51):
            self.deck.deal()
        # expect no error when no cards are in the deck
        self.assertEqual(self.deck.search(top_card), -1)

    def test_deck_reorder(self):
        self.assertNotEqual(self.deck.deck[-1], self.card)
        self.deck.shuffle()
        dealt_card = self.deck.deal()
        self.deck.new_order()

        self.assertEqual(len(self.deck.deck), 51)
        self.assertEqual(self.deck.search(dealt_card), -1)

        self.assertEqual(self.deck.deck[-1], self.card)
