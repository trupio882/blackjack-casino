import pytest
from bet_manager import BetManager
from player import Player, Hand

class TestBetManager:
    def test_bet_manager_initialization(self):
        bm = BetManager(10, 1000)
        assert bm.min_bet == 10
        assert bm.max_bet == 1000

    def test_bet_valid(self):
        player = Player("Test", 500)
        bm = BetManager(10, 1000)
        hand = player.hands.last_hand
        
        result = bm.bet(player, 100)
        assert result is True
        assert player.balance == 400
        assert hand.bet == 100

    def test_bet_below_min(self):
        player = Player("Test", 500)
        bm = BetManager(10, 1000)
        
        result = bm.bet(player, 5)
        assert result is False
        assert player.balance == 500

    def test_bet_above_max(self):
        player = Player("Test", 500)
        bm = BetManager(10, 1000)
        
        result = bm.bet(player, 1500)
        assert result is False
        assert player.balance == 500

    def test_bet_insufficient_funds(self):
        player = Player("Test", 50)
        bm = BetManager(10, 1000)
        
        result = bm.bet(player, 100)
        assert result is False
        assert player.balance == 50

    def test_blackjack_payout(self):
        player = Player("Test", 1000)
        bm = BetManager(10, 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        
        bm.black_jack(player, hand)
        assert player.balance == 1150  # 1000 + 100 + 50 (3:2)

    def test_resolve_main_bet_win(self):
        player = Player("Test", 1000)
        bm = BetManager(10, 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        
        bm.resolve_main_bet(player, hand, True)
        assert player.balance == 1200  # 1000 + 200

    def test_resolve_main_bet_loss(self):
        player = Player("Test", 1000)
        bm = BetManager(10, 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        
        bm.resolve_main_bet(player, hand, False)
        assert player.balance == 1000  # unchanged (already withdrawn)

    def test_resolve_main_bet_tie(self):
        player = Player("Test", 1000)
        bm = BetManager(10, 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        
        bm.resolve_main_bet(player, hand, False, tie=True)
        assert player.balance == 1100  # 1000 + 100

    def test_withdraw_insurance(self):
        player = Player("Test", 1000)
        bm = BetManager(10, 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        
        bm.withdraw_insurance(player, hand)
        assert player.balance == 950
        assert hand.insurance is True

    def test_deposit_insurance(self):
        player = Player("Test", 1000)
        bm = BetManager(10, 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        
        bm.deposit_insurance(player, hand)
        assert player.balance == 1100  # 1000 + 100

    def test_can_bet_for_insurance_true(self):
        player = Player("Test", 100)
        bm = BetManager(10, 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        
        assert bm.can_bet_for_insurance(player, hand) is True

    def test_can_bet_for_insurance_false(self):
        player = Player("Test", 40)
        bm = BetManager(10, 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        
        assert bm.can_bet_for_insurance(player, hand) is False

    def test_double_bet(self):
        player = Player("Test", 1000)
        bm = BetManager(10, 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        
        bm.double_bet(player, hand)
        assert player.balance == 900
        assert hand.bet == 200

    def test_double_bet_insufficient_funds(self):
        player = Player("Test", 50)
        bm = BetManager(10, 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        
        with pytest.raises(ValueError, match="Insufficient funds"):
            bm.double_bet(player, hand)