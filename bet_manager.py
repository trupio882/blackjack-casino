from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from player import Player, Hand


class BetManager:
    """Handles betting: placing, doubling, insurance, and payouts."""

    def __init__(self, min_bet: int = 10, max_bet: int = 1000) -> None:
        self.min_bet: int = min_bet
        self.max_bet: int = max_bet
    
    def place_initial_bet(self, player: 'Player') -> None:
        """Ask the player for an initial bet and deduct it."""
        if player.balance < self.min_bet:
            raise ValueError(f"Insufficient funds. Minimum bet: {self.min_bet}")
        
        while True:
            try:
                amount = int(input(f"\n{player.name} (balance {player.balance}) "
                                   f"Bet [{self.min_bet}..{self.max_bet}]: "))
                if amount < self.min_bet:
                    print(f"Minimum bet is {self.min_bet}")
                elif amount > self.max_bet:
                    print(f"Maximum bet is {self.max_bet}")
                else:
                    break
            except ValueError:
                print("Please enter an integer.")
        
        self.withdraw(player, amount)
        player.hands.tail.bet = amount
    
    def black_jack(self, player: 'Player', hand: 'Hand') -> None:
        """Payout 3:2 for a blackjack."""
        win = hand.bet + hand.bet * 3 // 2
        print(f"{player.name}, blackjack! You win {win}")
        player.deposit(win)
    
    def resolve_main_bet(self, player: 'Player', hand: 'Hand', win: bool, tie: bool = False) -> None:
        """Resolve the main bet: win, lose, or push."""
        bet = hand.bet
        win_bet = bet*2

        if win:
            self.deposit(player, win_bet)
            print(f"{player.name} wins {win_bet}!")
        elif tie:
            print("Push, bet returned.")
            self.deposit(player, bet)
        else:
            print(f"{player.name} loses {bet}.")
    
    def withdraw(self, player: 'Player', bet: int) -> None:
        player.withdraw(bet)
    
    def deposit(self, player: 'Player', bet: int) -> None:
        player.deposit(bet)
    
    def withdraw_insurance(self, player: 'Player', hand: 'Hand') -> None:
        """Deduct insurance premium (half the bet)."""
        bet = hand.bet
        self.withdraw(player, bet//2)
        hand.insurance = True

    def deposit_insurance(self, player: 'Player', hand: 'Hand') -> None:
        """Payout insurance (2:1)."""
        win = hand.bet
        self.deposit(player, win)
        print(f"{player.name}, insurance pays {win}")

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
        
        self.withdraw(player, bet)
        hand.bet = bet * 2
     
