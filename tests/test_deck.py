import pytest
from deck_for_black_jack import Deck, Card

class TestDeck:
    def test_deck_initialization(self):
        deck = Deck(num_decks=1)
        assert len(deck.cards) == 52
        
    def test_deck_with_multiple_decks(self):
        deck = Deck(num_decks=4)
        assert len(deck.cards) == 208
        
    def test_card_deal(self):
        deck = Deck()
        card = deck.card_deal()
        assert isinstance(card, Card)
        assert len(deck.cards) == 51
        
    def test_deck_update(self):
        deck = Deck(num_decks=1)
        # Оставляем мало карт
        for _ in range(40):
            deck.card_deal()
        deck.update_deck()  # Должна пересобрать
        assert len(deck.cards) > 50

class TestCard:
    def test_card_value(self):
        assert Card("♠", "A").value() == 11
        assert Card("♠", "K").value() == 10
        assert Card("♠", "5").value() == 5