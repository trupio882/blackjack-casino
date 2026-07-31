import pytest
from unittest.mock import Mock, patch
from game import Black_jack
from player import Player, Hand
from blackjack_deck import Card, Deck

class TestBlackJack:
    def test_game_initialization(self):
        game = Black_jack(10, 1000, 5)
        assert game.bet_manager.min_bet == 10
        assert game.bet_manager.max_bet == 1000
        assert game.table_hands_limit == 5
        assert game.dealer.name == "Dealer"

    def test_add_player(self):
        game = Black_jack(10, 1000, 5)
        player = Player("Test", 1000)
        game.add_player(player)
        assert len(game.players) == 1
        assert game.players[0].name == "Test"

    def test_add_player_insufficient_balance(self, capsys):
        game = Black_jack(100, 1000, 5)
        player = Player("Test", 50)
        game.add_player(player)
        
        captured = capsys.readouterr()
        assert "cannot play" in captured.out
        assert len(game.players) == 0

    def test_add_player_limit(self):
        game = Black_jack(10, 1000, 1)  # limit 1
        player1 = Player("Test1", 1000)
        player2 = Player("Test2", 1000)
        
        game.add_player(player1)
        game.add_player(player2)
        
        assert len(game.players) == 1
        assert game.players[0].name == "Test1"

    def test_dealer_have_blackjack(self):
        game = Black_jack(10, 1000, 5)
        player = Player("Test", 1000)
        hand = Hand()
        hand.bet = 100
        hand.add_card(Card("♠", "A"))
        hand.add_card(Card("♠", "K"))
        
        # Mock dealer blackjack
        game.dealer.get_first_hand().add_card(Card("♠", "A"))
        game.dealer.get_first_hand().add_card(Card("♠", "K"))
        
        # Should not raise any exception
        game._dealer_have_blackjack(player, hand)

    def test_check_winner_player_blackjack(self):
        game = Black_jack(10, 1000, 5)
        player = Player("Test", 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        hand.add_card(Card("♠", "A"))
        hand.add_card(Card("♠", "K"))
        
        game.players.append(player)
        game._check_winner(player)
        assert player.balance == 1150  # 1000 + 100 + 50 (3:2)

    def test_check_winner_player_bust(self):
        game = Black_jack(10, 1000, 5)
        player = Player("Test", 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        hand.add_card(Card("♠", "10"))
        hand.add_card(Card("♥", "J"))
        hand.add_card(Card("♦", "Q"))
        
        game.players.append(player)
        game._check_winner(player)
        assert player.balance == 1000  # unchanged (already withdrawn)

    def test_check_winner_player_wins(self):
        game = Black_jack(10, 1000, 5)
        player = Player("Test", 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        hand.add_card(Card("♠", "10"))
        hand.add_card(Card("♥", "9"))
        
        # Dealer has lower score
        game.dealer.get_first_hand().add_card(Card("♠", "5"))
        game.dealer.get_first_hand().add_card(Card("♥", "6"))
        
        game.players.append(player)
        game._check_winner(player)
        assert player.balance == 1200  # 1000 + 200

    def test_check_winner_player_loses(self):
        game = Black_jack(10, 1000, 5)
        player = Player("Test", 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        hand.add_card(Card("♠", "10"))
        hand.add_card(Card("♥", "9"))
        
        # Dealer has higher score
        game.dealer.get_first_hand().add_card(Card("♠", "10"))
        game.dealer.get_first_hand().add_card(Card("♥", "J"))
        
        game.players.append(player)
        game._check_winner(player)
        assert player.balance == 1000  # unchanged (already withdrawn)

    def test_check_winner_tie(self):
        game = Black_jack(10, 1000, 5)
        player = Player("Test", 1000)
        hand = player.hands.last_hand
        hand.bet = 100
        hand.add_card(Card("♠", "10"))
        hand.add_card(Card("♥", "9"))
        
        # Dealer has same score
        game.dealer.get_first_hand().add_card(Card("♠", "10"))
        game.dealer.get_first_hand().add_card(Card("♥", "9"))
        
        game.players.append(player)
        game._check_winner(player)
        assert player.balance == 1100  # 1000 + 100 (tie)

    def test_player_action_stand(self, monkeypatch):
        game = Black_jack(10, 1000, 5)
        player = Player("Test", 1000)
        hand = player.hands.last_hand
        hand.add_card(Card("♠", "10"))
        hand.add_card(Card("♥", "9"))
        
        # Mock user input for 's' (stand)
        monkeypatch.setattr('builtins.input', lambda _: 's')
        
        # Should not raise any exception
        game._player_action(player, hand, 1)

    def test_player_action_hit_then_stand(self, monkeypatch):
        game = Black_jack(10, 1000, 5)
        player = Player("Test", 1000)
        hand = player.hands.last_hand
        hand.add_card(Card("♠", "5"))
        hand.add_card(Card("♥", "6"))
        
        # Mock user input for 'h' then 's'
        inputs = ['h', 's']
        monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
        
        # Should not raise any exception
        game._player_action(player, hand, 1)

    def test_show_hand(self, capsys):
        game = Black_jack(10, 1000, 5)
        player = Player("Test", 1000)
        hand = player.hands.last_hand
        hand.add_card(Card("♠", "A"))
        hand.add_card(Card("♥", "K"))
        
        game.dealer.get_first_hand().add_card(Card("♠", "10"))
        game.dealer.get_first_hand().add_card(Card("♥", "9"))
        
        game._show_hand(player, hand, 1, show_dealer=True)
        captured = capsys.readouterr()
        assert "Test" in captured.out
        assert "A♠" in captured.out
        assert "K♥" in captured.out