from money import Money
from deck_for_black_jack import Card
from typing import Optional, List


class Player:
    """A Blackjack player."""

    def __init__(self, name: str, money: int = 1000) -> None:
        self.name: str = name
        self.hands: HandList = HandList()
        self._money: Money = Money(money)
    
    def get_first_hand(self) -> Optional['Hand']:
        return self.hands.head
    
    def reset_hand(self) -> None:
        self.hands = HandList()
    
    def deposit(self, amount: int) -> None:
        self._money.deposit(amount)

    def withdraw(self, amount: int) -> None:
        self._money.withdraw(amount)
    
    def create_split_hand(self, hand: 'Hand') -> 'Hand':
        """Split a hand: take one card and create a new hand."""
        if not isinstance(hand, Hand):
            raise TypeError("hand must be a Hand instance")
        
        if not hand.can_split():
            raise ValueError("This hand cannot be split")
        
        split_card = hand.cards.pop()
        new_hand = self.hands.add_hand(hand)
        new_hand.cards.append(split_card)
        new_hand.bet = hand.bet
        return new_hand

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, nick: str) -> None:
        if not (isinstance(nick, str) and nick.strip() and not nick.isdigit()):
            raise ValueError("Name must be a non-empty string, not just digits")
        
        self._name = nick

    @property
    def balance(self) -> int:
        return self._money.money

class HandList:
    """Linked list of hands for a player."""
    
    def __init__(self) -> None:
        self.length = 1
        self.hand: 'Hand' = Hand()
        self.head: 'Hand' = self.hand
        self.tail: 'Hand' = self.head
    
    def add_hand(self, insert_after: Optional['Hand'] = None) -> 'Hand':
        """Add a new hand after the given hand (or at the end)."""
        if insert_after is not None and not isinstance(insert_after, Hand):
            raise ValueError("insert_after must be a Hand or None")

        new_hand = Hand()

        if insert_after:
            new_hand.next = insert_after.next
            insert_after.next = new_hand
            if insert_after == self.tail:
                self.tail = new_hand
        else:
            self.tail.next = new_hand
            self.tail = new_hand
        
        self.length += 1
        return new_hand
    
    def __len__(self) -> int:
        return self.length


class Hand:
    """A single hand of cards for a player."""

    def __init__(self) -> None:
        self.next: Optional['Hand'] = None
        self.bet: int = 0
        self.cards: List[Card] = []
        self.insurance: bool = False
    
    def is_black_jack(self) -> bool:
        """Return True if the hand is a natural blackjack (two cards, total 21)."""
        return len(self.cards) == 2 and self.calculate_card() == 21
        
    def can_split(self) -> bool:
        """Return True if the two cards have the same rank."""
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank
    
    def add_card(self, card: Card) -> None:
        if not isinstance(card, Card):
            raise TypeError("card must be a Card instance")
        
        self.cards.append(card)
    
    def calculate_card(self) -> int:
        """Compute the total value of the hand, adjusting Aces from 11 to 1 as needed."""
        aces = 0
        score = 0

        for card in self.cards:
            score += card.value()

            if card.rank == "A":
                aces += 1

        while score > 21 and aces:
            score -= 10
            aces -= 1

        return score

    def display_hand(self) -> str:
        return ", ".join([str(card) for card in self.cards])