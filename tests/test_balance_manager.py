import pytest
from unittest.mock import patch
from balance_manager import Deposit
from player import Player

class TestDeposit:
    def test_deposit_initialization(self):
        dep = Deposit(500)
        assert dep.amount == 500

    def test_deposit_initialization_default(self):
        dep = Deposit()
        assert dep.amount == 500

    def test_deposit_invalid_amount(self):
        with pytest.raises(ValueError, match="positive integer"):
            Deposit(0)
        
        with pytest.raises(ValueError, match="positive integer"):
            Deposit(-100)
        
        with pytest.raises(ValueError, match="positive integer"):
            Deposit("500")  # type: ignore

    def test_deposit_valid_card(self):
        dep = Deposit(500)
        player = Player("Test", 1000)
        
        # Mock user inputs
        with patch('builtins.input', side_effect=[
            "1234 5678 9012 3456",  # card number
            "12/25",                # expiry
            "123"                   # CVV
        ]):
            dep.deposit(player)
            assert player.balance == 1500

    def test_deposit_cancel_card(self):
        dep = Deposit(500)
        player = Player("Test", 1000)
        initial_balance = player.balance
        
        with patch('builtins.input', side_effect=["0"]):
            dep.deposit(player)
            assert player.balance == initial_balance

    def test_deposit_cancel_expiry(self):
        dep = Deposit(500)
        player = Player("Test", 1000)
        initial_balance = player.balance
        
        with patch('builtins.input', side_effect=[
            "1234 5678 9012 3456",
            "0"
        ]):
            dep.deposit(player)
            assert player.balance == initial_balance

    def test_deposit_cancel_cvv(self):
        dep = Deposit(500)
        player = Player("Test", 1000)
        initial_balance = player.balance
        
        with patch('builtins.input', side_effect=[
            "1234 5678 9012 3456",
            "12/25",
            "0"
        ]):
            dep.deposit(player)
            assert player.balance == initial_balance

    def test_deposit_invalid_card_format(self):
        dep = Deposit(500)
        player = Player("Test", 1000)
        
        with patch('builtins.input', side_effect=[
            "1234 5678 9012",       # invalid (3 groups)
            "1234 5678 9012 3456",  # valid
            "12/25",
            "123"
        ]):
            dep.deposit(player)
            assert player.balance == 1500

    def test_deposit_invalid_expiry_format(self):
        dep = Deposit(500)
        player = Player("Test", 1000)
        
        with patch('builtins.input', side_effect=[
            "1234 5678 9012 3456",
            "12-25",                # invalid
            "12/25",                # valid
            "123"
        ]):
            dep.deposit(player)
            assert player.balance == 1500

    def test_deposit_invalid_cvv_format(self):
        dep = Deposit(500)
        player = Player("Test", 1000)
        
        with patch('builtins.input', side_effect=[
            "1234 5678 9012 3456",
            "12/25",
            "12",                   # invalid (2 digits)
            "123"                   # valid
        ]):
            dep.deposit(player)
            assert player.balance == 1500

    def test_deposit_with_non_player(self):
        dep = Deposit(500)
        
        with pytest.raises(TypeError, match="player must be a Player instance"):
            dep.deposit("not a player")  # type: ignore