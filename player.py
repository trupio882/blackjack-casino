from save_manager import SaveManager
from blackjack_deck import Card
from typing import Optional, List

class BalanceDescriptor:
    """Descriptor for managing player balance with auto-save."""
    def __set_name__(self, owner, name):
        self.name = "_" + name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        return getattr(instance, self.name, 0)
    
    def __set__(self, instance, value):
        if instance is None:
            return self
        
        if value < 0:
            raise ValueError("Balance cannot be negative")
        
        setattr(instance, self.name, value)
        
        # Auto-save balance if save_manager exists
        if hasattr(instance, '_save_manager'):
            try:
                instance._save_manager.update_player_balance(instance)
            except Exception as e:
                print(f"Warning: Could not save balance: {e}")
        else:
            pass
    

class Player:
    """A Blackjack player."""
    balance = BalanceDescriptor()

    def __init__(self, name: str, money: int = 1000) -> None:
        self.name: str = name
        self.in_game: bool = True
        self._hands: HandList = HandList()
        self._save_manager: SaveManager = SaveManager()
        self.balance = money
    
    def get_first_hand(self) -> Optional['Hand']:
        return self._hands.first_hand
    
    def reset_hand(self) -> None:
        self._hands = HandList()
    
    def create_split_hand(self, hand: 'Hand') -> 'Hand':
        """Split a hand: take one card and create a new hand."""
        if not isinstance(hand, Hand):
            raise TypeError("hand must be a Hand instance")

        if not self._hands._contains(hand):
            raise ValueError("Hand does not belong to this player")
        
        if not hand.can_split():
            raise ValueError("This hand cannot be split")
        
        split_card = hand.pop_last_card()
        new_hand = self._hands.add_hand(hand)
        new_hand.add_card(split_card)
        new_hand.bet = hand.bet
        return new_hand

    def deposit(self, value: int) -> None:
        """Add money to the balance."""
        self.__validate_pos_int(value)
        self.balance += value  

    def withdraw(self, value: int) -> None:
        """Subtract money from the balance."""
        self.__validate_pos_int(value)
        
        if value > self.balance:
            raise ValueError(f"Insufficient funds. Available: {self.balance}, requested: {value}")
    
        self.balance -= value

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, nick: str) -> None:
        if not (isinstance(nick, str) and nick.strip()):
            raise ValueError("name must be a non-empty string")
        
        self._name = nick
    
    @property
    def hands(self) -> 'HandList':
        return self._hands
    
    @property
    def in_game(self) -> bool:
        return self._in_game
    
    @in_game.setter
    def in_game(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError
        
        self._in_game = value
    
    @staticmethod
    def __validate_pos_int(value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("Amount must be a non-negative integer.")

class HandList:
    """Linked list of hands for a player."""
    
    def __init__(self) -> None:
        self._length: int = 1
        self._head: 'Hand' = Hand()
        self._tail: 'Hand' = self._head

    def __len__(self) -> int:
        return self._length
    
    def add_hand(self, insert_after: Optional['Hand'] = None) -> 'Hand':
        """Add a new hand after the given hand (or at the end)."""
        if insert_after is not None and not isinstance(insert_after, Hand):
            raise ValueError("insert_after must be a Hand or None")

        new_hand = Hand()

        if insert_after:
            new_hand.next_hand = insert_after.next_hand
            insert_after.next_hand = new_hand

            if insert_after == self._tail:
                self._tail = new_hand
        else:
            self._tail.next_hand = new_hand
            self._tail = new_hand
        
        self._length += 1
        return new_hand
    
    def _contains(self, hand: 'Hand') -> bool:
        """Check if a hand exists in the linked list."""
        current = self._head

        while current:
            if current is hand:
                return True
            
            current = current.next_hand

        return False

    @property
    def hand(self) -> 'Hand':
        return self._head

    @property
    def length(self) -> int:
        return self._length
    
    @property
    def first_hand(self) -> 'Hand':
        return self._head
    
    @property
    def last_hand(self) -> 'Hand':
        return self._tail

class Hand:
    """A single hand of cards for a player."""

    def __init__(self) -> None:
        self._next: Optional['Hand'] = None
        self._bet: int = 0
        self._cards: List[Card] = []
        self.insurance: bool = False
    
    def is_blackjack(self) -> bool:
        """Return True if the hand is a natural blackjack (two cards, total 21)."""
        return len(self._cards) == 2 and self.calculate_card() == 21
        
    def can_split(self) -> bool:
        """Return True if the two cards have the same rank."""
        return len(self._cards) == 2 and self._cards[0].rank == self._cards[1].rank
    
    def add_card(self, card: Card) -> None:
        if not isinstance(card, Card):
            raise TypeError("card must be a Card instance")
        
        self._cards.append(card)

    def pop_last_card(self) -> Card:
        if not self._cards:
            raise IndexError("Cannot pop from empty hand")
        
        return self._cards.pop()
    
    def calculate_card(self) -> int:
        """Compute the total value of the hand, adjusting Aces from 11 to 1 as needed."""
        aces = 0
        score = 0

        for card in self._cards:
            score += card.value()

            if card.rank == "A":
                aces += 1

        while score > 21 and aces:
            score -= 10
            aces -= 1

        return score
    
    def get_first_card(self) -> Card:
        if not self._cards:
            raise IndexError("No Cards")
        
        return self._cards[0]

    def display_hand(self) -> str:
        return ", ".join([str(card) for card in self._cards])
    
    @property
    def cards(self) -> List[Card]:
        return self._cards[:]
    
    @property
    def next_hand(self) -> 'Hand':
        return self._next
    
    @next_hand.setter
    def next_hand(self, node: 'Hand'):
        if not (isinstance(node, Hand) or node is None):
            raise ValueError("next_hand must be a Hand instance or None")
        
        self._next = node
    
    @property
    def bet(self) -> int:
        return self._bet
    
    @bet.setter
    def bet(self, amount: int):
        if not (isinstance(amount, int) and amount > 0):
            raise ValueError("Bet must be a positive integer")
        
        self._bet = amount

    @property
    def insurance(self) -> bool:
        return self._insurance
    
    @insurance.setter
    def insurance(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Insurance must be a boolean value")
        
        self._insurance = value