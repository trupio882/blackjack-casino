import pytest
from player import Player, Hand
from deck_for_black_jack import Card

class TestPlayer:
    def test_player_creation(self):
        player = Player("Test", 1000)
        assert player.name == "Test"
        assert player.balance == 1000
        
    def test_deposit(self):
        player = Player("Test", 1000)
        player.deposit(500)
        assert player.balance == 1500
        
    def test_withdraw(self):
        player = Player("Test", 1000)
        player.withdraw(300)
        assert player.balance == 700
        
    def test_split_hand(self):
        player = Player("Test")
        hand = Hand()
        hand.cards = [Card("♠", "8"), Card("♥", "8")]
        hand.bet = 100
        
        new_hand = player.create_split_hand(hand)
        assert len(hand.cards) == 1
        assert len(new_hand.cards) == 1
        assert new_hand.bet == 100