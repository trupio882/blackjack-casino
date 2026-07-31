import random
import time
from typing import List


class Card:
    """A single playing card for Blackjack."""

    def __init__(self, suit: str, rank: str) -> None:
        self.suit: str = suit
        self.rank: str = rank

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def value(self):
        """Return numeric value of the card (10 for face cards, 11 for Ace, else rank)."""
        if self.rank in ("J", "Q", "K"):
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)

class Deck:
    """A deck composed of multiple standard 52-card decks."""

    SUITS: List[str] = ["♣", "♥", "♦", "♠"]
    RANKS: List[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K", "A"]
    SHUFFLE_TIME: int = 2

    def __init__(self, num_decks: int = 4) -> None:
        self.num_decks: int = num_decks
        self.build_new_deck()

    def build_new_deck(self) -> None:
        """Create a fresh shuffled deck."""
        self.cards = [Card(suit, rank) for suit in Deck.SUITS for rank in Deck.RANKS] * self.num_decks
        self.shuffle()
    
    def update_deck(self) -> None:
        """Replace deck if less than half cards remain, with a 2-second delay."""
        if len(self.cards) < len(Deck.SUITS) * len(Deck.RANKS) * self.num_decks // 2:
           print("Waiting 2 seconds, changing deck...")
           time.sleep(self.SHUFFLE_TIME)
           print("New deck built and shuffled.")
           self.build_new_deck()

    def shuffle(self) -> None:
        """Randomly shuffle the cards."""
        random.shuffle(self.cards)

    def card_deal(self) -> 'Card':
        """Deal one card from the top."""
        if not self.cards:
            raise IndexError("Deck is empty! Call update_deck().")
        
        return self.cards.pop()