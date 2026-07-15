class Money:
    """Manage a player's money balance."""

    def __init__(self, money: int = 1000) -> None:
        self.money: int = money

    def deposit(self, value: int) -> None:
        """Add money to the balance."""
        self.__validate_pos_int(value)
        self.money += value  

    def withdraw(self, value: int) -> None:
        """Subtract money from the balance."""
        self.__validate_pos_int(value)
        
        if value > self._money:
            raise ValueError(f"Insufficient funds. Available: {self._money}, requested: {value}")
    
        self.money -= value

    @property
    def money(self) -> int:
        return self._money
    
    @money.setter
    def money(self, value: int) -> None:
        self.__validate_pos_int(value)
        self._money = value
    
    @staticmethod
    def __validate_pos_int(value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("Amount must be a non-negative integer.")