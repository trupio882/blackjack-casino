from player import Player
from ui import ConsoleUI

class Deposit:
    """Simulate depositing money via card details."""
    ui = ConsoleUI()

    def __init__(self, amount: int = 500) -> None:
        self.amount: int = amount
    
    def deposit(self, player: Player) -> None:
        """Process deposit after entering card details."""
        if not isinstance(player, Player):
            raise TypeError("player must be a Player instance")
        
        self.ui.show_start_message_app_balance(self.amount)

        # Card number
        while True:
            num_card = self.ui.input_num_card()

            if num_card == "0":
                return
            
            split_num_car = num_card.split()

            if len(split_num_car) == 4 and all(map(lambda x: len(x) == 4 and x.isdigit(), split_num_car)):
                break
            
            if len(num_card) == 16 and num_card.isdigit():
                break

            self.ui.show_num_card_error()
        
        # Expiry date
        while True:
            date_card = self.ui.input_card_date()

            if date_card == "0":
                return

            if all(map(lambda x: len(x) == 2 and x.isdigit(), date_card.split("/"))):
                break

            self.ui.show_card_date_error()
        
        # CVV
        while True:
            cvv = self.ui.input_cvv()

            if cvv == "0":
                return
            
            if len(cvv) == 3 and cvv.isdigit():
                break

            self.ui.show_cvv_error()

        player.deposit(self.amount)
        self.ui.show_finall_message_app_balance(player, self.amount)
    
    @property
    def amount(self) -> int:
        return self.__amount
    
    @amount.setter
    def amount(self, num: int) -> None:
        if not isinstance(num, int) or num <= 0:
            raise ValueError("Amount must be a positive integer.")
        
        self.__amount = num