from player import Player

class Deposit:
    """Simulate depositing money via card details."""

    def __init__(self, amount: int = 500) -> None:
        self.amount: int = amount
    
    def deposit(self, player: Player) -> None:
        """Process deposit after entering card details."""
        if not isinstance(player, Player):
            raise TypeError("player must be a Player instance")

        print(f"\n{self.amount} will be charged to your card.")

        # Card number
        while True:
            num_card = input("\nEnter card number (16 digits) or 0 to cancel: ").strip()

            if num_card == "0":
                return
            
            split_num_car = num_card.split()

            if len(split_num_car) == 4 and all(map(lambda x: len(x) == 4 and x.isdigit(), split_num_car)):
                break
            
            if len(num_card) == 16 and num_card.isdigit():
                break

            print("Card number must be exactly 16 digits.\n")
        
        # Expiry date
        while True:
            date_card = input("\nEnter expiry date (MM/YY) or 0 to cancel: ").strip()

            if date_card == "0":
                return
            
            if all(map(lambda x: len(x) == 2 and x.isdigit(), date_card.split("/"))):
                break

            print("Date must be in format MM/YY (e.g., 12/25).")
        
        # CVV
        while True:
            cvv = input("\nEnter CVV (3 digits) or 0 to cancel: ").strip()

            if cvv == "0":
                return
            
            if len(cvv) == 3 and cvv.isdigit():
                break

            print("CVV must be 3 digits.")

        player.deposit(self.amount)
        print(f"{player.name}'s balance increased by {self.amount}")
    
    @property
    def amount(self) -> int:
        return self.__amount
    
    @amount.setter
    def amount(self, num: int) -> None:
        if not isinstance(num, int) or num <= 0:
            raise ValueError("Amount must be a positive integer.")
        
        self.__amount = num