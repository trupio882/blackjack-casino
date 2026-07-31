from ui import ConsoleUI
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from player import Player, Hand

class BetManager:
    """Handles betting: placing, doubling, insurance, and payouts."""
    ui: ConsoleUI = ConsoleUI()

    def __init__(self, min_bet: int = 10, max_bet: int = 1000) -> None:
        self.min_bet: int = min_bet
        self.max_bet: int = max_bet
    
    def bet(self, player: 'Player', amount: int) -> bool:
        """Place a bet for the player."""
        if amount < self.min_bet:
            self.ui.show_min_bet(self.min_bet)
            return False
        elif amount > self.max_bet:
            self.ui.show_max_bet(self.max_bet)
            return False
        elif amount > player.balance:
            self.ui.enough_balance(player.balance)
            return False
        else:
            player.withdraw(amount)
            player.hands.last_hand.bet = amount
            return True 
    
    def blackjack(self, player: 'Player', hand: 'Hand') -> None:
        """Payout 3:2 for a blackjack."""
        win = hand.bet + hand.bet * 3 // 2
        self.ui.show_blackjack_win(player.name, win)
        player.deposit(win)
    
    def resolve_main_bet(self, player: 'Player', hand: 'Hand', win: bool, tie: bool = False) -> None:
        """Resolve the main bet: win, lose, or push."""
        bet = hand.bet
        win_bet = bet*2

        if win:
            player.deposit(win_bet)
            self.ui.show_win(player.name, win_bet)
        elif tie:
            self.ui.show_tie(player.name, bet)
            player.deposit(bet)
        else:
            self.ui.show_lose(player.name, bet)
    
    def withdraw_insurance(self, player: 'Player', hand: 'Hand') -> None:
        """Deduct insurance premium (half the bet)."""
        bet = hand.bet
        player.withdraw(bet//2)
        hand.insurance = True

    def deposit_insurance(self, player: 'Player', hand: 'Hand') -> None:
        """Payout insurance (2:1)."""
        win = hand.bet
        player.deposit(win)
        self.ui.show_pushout_insurance(player.name, win)

    def can_bet_for_insurance(self, player: 'Player', hand: 'Hand') -> bool:
        return hand.bet // 2 <= player.balance

    def can_bet_for_split_double(self, player: 'Player', hand: 'Hand') -> bool:
        return hand.bet <= player.balance

    def double_bet(self, player: 'Player', hand: 'Hand') -> None:
        """Double the bet (withdraw an additional amount equal to the bet)."""
        bet = hand.bet

        if hand.bet <= 0:
            raise ValueError("Bet must be positive.")
        
        if hand.bet > player.balance:
            raise ValueError(f"Insufficient funds to double. Need: {hand.bet}, have: {player.balance}")
        
        player.withdraw(bet)
        hand.bet = bet * 2
    
    def withdraw_split(self, player: 'Player', hand: 'Hand') -> None:
        if hand.bet <= 0:
            raise ValueError("Bet must be positive.")
        
        if hand.bet > player.balance:
            raise ValueError(f"Insufficient funds to double. Need: {hand.bet}, have: {player.balance}")
        
        bet = hand.bet
        player.withdraw(bet)
    
    @property
    def min_bet(self) -> int:
        return self._min_bet
    
    @min_bet.setter
    def min_bet(self, amount: int) -> None:
        if not (isinstance(amount, int) and amount > 0):
            raise ValueError
        
        self._min_bet = amount
    
    @property
    def max_bet(self) -> int:
        return self._max_bet
    
    @max_bet.setter
    def max_bet(self, amount: int) -> None:
        if not (isinstance(amount, int) and amount > 0):
            raise ValueError
        
        self._max_bet = amount