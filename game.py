from typing import List, Optional
from deck_for_black_jack import Deck, Card
from bet_manager import BetManager
from player import Player, Hand

class Black_jack:
    """Main Blackjack game logic."""

    def __init__(self, min_bet: int = 10, max_bet: int = 1000, table_hands_limit: int = 5) -> None:
        self.table_hands_limit: int = table_hands_limit
        self.deck: Deck = Deck()
        self.dealer: Player = Player("Dealer")
        self.players: List[Player] = []
        self.bet_manager: BetManager = BetManager(min_bet, max_bet)

    def start_game(self) -> None:
        """Run a full round of Blackjack."""
        self.deck.update_deck()

        # Reset all hands
        for player in self.players:
            player.reset_hand()

        self.dealer.reset_hand()

        # Collect bets and offer extra hands
        for player in self.players:
            if player.balance < self.bet_manager.min_bet:
                print(f"{player.name} cannot play: balance {player.balance} < min bet {self.bet_manager.min_bet}")
                return
            
            self.bet_manager.place_initial_bet(player)

            # Additional hands (splits)
            while True:
                total_hands = sum(len(p.hands) for p in self.players)
                if player.balance >= self.bet_manager.min_bet and total_hands + 1 <= self.table_hands_limit:
                    choice = input(f"{player.name}, add another hand? (y/n): ").strip().lower()

                    if choice == 'y':
                        player.hands.add_hand()
                        self.bet_manager.place_initial_bet(player)
                    elif choice == 'n':
                        break
                    else:
                        print("Please enter 'y' or 'n'.")
                else:
                    break       
        
            # Deal two cards to each player and dealer
            hand = player.hands.hand

            while hand:
                for _ in range(2):
                    hand.add_card(self.deck.card_deal())
                
                hand = hand.next
        
        for _ in range(2):
            self.dealer.get_first_hand().add_card(self.deck.card_deal())

        # Insurance if dealer shows an Ace
        if self.dealer.get_first_hand().cards[0].rank == "A":
            for player in self.players:
                hand_num = 1
                hand = player.hands.hand

                while hand:
                    self.insurance(player, hand, hand_num)
                    hand = hand.next
                    hand_num += 1
            
            if self.dealer.get_first_hand().is_black_jack():
                for player in self.players:
                    self.check_winner(player) 
                    
                self.ask_continue()
                return

        # Players' turns
        for player in self.players:
            hand = player.hands.hand
            hand_num = 1

            while hand:
                self.play_hand(player, hand, hand_num)
                hand = hand.next
                hand_num += 1

        # Dealer draws until 17+
        dealer_hand = self.dealer.get_first_hand()

        while dealer_hand.calculate_card() < 17:
            dealer_hand.add_card(self.deck.card_deal())

        # Determine winners
        for player in self.players:
            self.check_winner(player) 
            
        self.ask_continue()
        return
    
    def insurance(self, player: Player, hand: Hand, hand_num: int) -> None:
        """Offer insurance to the player."""
        while True:
            self.show_hand(player, hand, hand_num)

            if not self.bet_manager.can_bet_for_insurance(player, hand):
                print(f"{player.name}, hand {hand_num}: not enough money for insurance.")
                return
            
            choice = input(f"Buy insurance for {hand.bet//2}? (y/n): ").strip().lower()

            if choice == "y":
                self.bet_manager.withdraw_insurance(player, hand)
                return
            elif choice == "n":
                return
            else:
                print("Enter 'y' or 'n'.")

    def play_hand(self, player: Player, hand: Hand, hand_num: int) -> None:
        """Handle a single hand's turn."""
        self.show_hand(player, hand, hand_num, show_dealer=False)

        if hand.calculate_card() == 21:
            print("Blackjack!")
            return
        
        can_bet_for_double_split = self.bet_manager.can_bet_for_split_double(player, hand)
        can_split = hand.can_split()
        bet = hand.bet
        double_txt = f", Double(d), for {bet}" if can_bet_for_double_split else ""
        split_txt = f", Split(1), for {bet}" if can_bet_for_double_split and can_split else ""

        while True:
            action = input(
                f"Hand {hand_num}:\n"
                f"Hit(h), Stand(s){double_txt}{split_txt}\n"
                "Your choice: "
            ).strip().lower()

            if action.lower() == "h":
                hand.add_card(self.deck.card_deal())
                self.player_action(player, hand, hand_num)
                return
            elif action.lower() == "d" and double_txt:
                self.bet_manager.double_bet(player, hand)
                hand.add_card(self.deck.card_deal())
                self.show_hand(player, hand, hand_num, show_dealer=False)
                return
            elif action.lower() == "1" and split_txt:
                if not can_split:
                    print("This hand cannot be split.")
                    continue
                    
                self.bet_manager.withdraw(player, bet)
                split_hand = player.create_split_hand(hand)
                
                hand.add_card(self.deck.card_deal())
                split_hand.add_card(self.deck.card_deal())

                self.play_hand(player, hand, hand_num)
                return
            elif action.lower() == "s":
                return
            else:
                print("\nInvalid input. Available: h, s, d, 1.\n")

    def player_action(self, player: Player, hand: Hand, hand_num: int) -> None:
        """Hit/Stand loop for a hand."""
        self.show_hand(player, hand, hand_num, show_dealer=False)

        while hand.calculate_card() <= 21:
            if hand.calculate_card() == 21:
                print(f"{player.name} ({hand_num}) have 21")
            while True:
                action = input("Hit(h) or Stand(s): ").strip().lower()

                if action == "h":
                    hand.add_card(self.deck.card_deal())
                    self.show_hand(player, hand, hand_num, show_dealer=False)
                    break
                elif action == "s":
                    return
                else:
                    print("Enter 'h' or 's'.")             
     
    def show_hand(self, player: Player, hand: Hand, hand_num: int, show_dealer: bool = False) -> None:
        """Display the player's hand and optionally the dealer's hand."""
        player_cards = hand.display_hand()
        player_score = hand.calculate_card()
        print(f"\n{player.name} (hand {hand_num}): {player_cards} | Score: {player_score}")
        dealer_hand = self.dealer.get_first_hand()

        if show_dealer:
            dealer_cards = dealer_hand.display_hand()
            dealer_score = dealer_hand.calculate_card()
            print(f"Dealer: {dealer_cards} | Score: {dealer_score}")
        else:
            first = str(dealer_hand.cards[0]) if dealer_hand.cards else "??"
            print(f"Dealer: {first}, [hidden card]")

    def _dealer_have_blackjack(self, player: Player, hand: Hand) -> None:
        """Handle case when dealer has blackjack."""
        if hand.insurance:
            self.bet_manager.deposit_insurance(player, hand)
        
        if hand.is_black_jack():
            self.bet_manager.resolve_main_bet(player, hand, False, tie=True)
            print("Push (both have blackjack).")
        else:
            self.bet_manager.resolve_main_bet(player, hand, False)
            print("Dealer has blackjack. You lose.")

    def check_winner(self, player: Player) -> None:
        """Evaluate all hands of a player against the dealer."""
        dealer_score = self.dealer.get_first_hand().calculate_card()
        print("\nFinal results:")

        hand = player.hands.hand
        hand_num = 1

        while hand:
            self.show_hand(player, hand, hand_num, show_dealer=True)
            card_score = hand.calculate_card()

            if self.dealer.get_first_hand().is_black_jack():
                self._dealer_have_blackjack(player, hand)
            elif hand.is_black_jack():
                self.bet_manager.black_jack(player, hand)
            elif hand.insurance:
                print(f"Insurance lost (lost {hand.bet//2}).")
            else:
                print(f"{player.name} score: {card_score}")
                print(f"{self.dealer.name}'s score: {dealer_score}")

                if card_score > 21:
                    print(f"{player.name} busted! Dealer win")
                    self.bet_manager.resolve_main_bet(player, hand, False)
                elif dealer_score > 21 or card_score > dealer_score:
                    self.bet_manager.resolve_main_bet(player, hand, True)
                    print(f"{player.name} win!!!")
                elif card_score < dealer_score:
                    self.bet_manager.resolve_main_bet(player, hand, False)
                    print(f"{player.name} lose. Dealer win")
                else:
                    self.bet_manager.resolve_main_bet(player, hand, False, tie=True)
                    print("It's a Tie")
            
            hand = hand.next
            hand_num += 1
        
        player.reset_hand()


    def ask_continue(self) -> None:
        """Ask if players want to continue playing."""
        while True:
            continue_game = input("\nPlay again? (y/n): ").strip().lower()

            if continue_game == "y":
                for player in self.players:
                    player.reset_hand()

                self.dealer.reset_hand()
                self.start_game()
                return
            elif continue_game == "n":
                self.players = []
                print("Thanks for playing!")
                return
            else:
                print("Enter 'y' or 'n'.")
    
    def add_player(self, player: Player) -> None:
        """Add a player to the table."""
        if not isinstance(player, Player):
            raise TypeError("player must be a Player instance")
        
        if player.balance < self.bet_manager.min_bet:
            print(f"{player.name} cannot play: balance {player.balance} < {self.bet_manager.min_bet}")
            return
        
        if len(self.players) >= self.table_hands_limit:
            print(f"Maximum number of players ({self.table_hands_limit}) reached.")
            return
        
        self.players.append(player)