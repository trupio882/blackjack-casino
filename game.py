from typing import List
from blackjack_deck import Deck
from bet_manager import BetManager
from ui import ConsoleUI
from player import Player, Hand

class BlackJack:
    """Main Blackjack game logic."""
    ui = ConsoleUI()

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
            player.in_game = True
            player.reset_hand()

        self.dealer.reset_hand()

        # Collect bets and offer extra hands
        for player in self.players:
            if player.balance < self.bet_manager.min_bet:
                self.ui.show_cannot_play(player, self.bet_manager.min_bet)
                player.in_game = False
                continue

            self._initial_bet(player)

            # Additional hands (splits)
            while True:
                total_hands = sum(len(p.hands) for p in self.players)
                
                if player.balance >= self.bet_manager.min_bet and total_hands + 1 <= self.table_hands_limit:
                    choice = self.ui.input_add_hand(player)

                    if choice == 'y':
                        player.hands.add_hand()
                        self._initial_bet(player)
                    elif choice == 'n':
                        break
                else:
                    break       
        
            # Deal two cards to each player and dealer
            hand = player.hands.hand

            while hand:
                for _ in range(2):    
                    hand.add_card(self.deck.card_deal())
                
                hand = hand.next_hand
        
        for _ in range(2):
            self.dealer.get_first_hand().add_card(self.deck.card_deal())

        # Insurance if dealer shows an Ace
        if self.dealer.get_first_hand().get_first_card().rank == "A":
            for player in self.players:
                if not player.in_game:
                    continue

                hand_num = 1
                hand = player.hands.hand

                while hand:
                    self._insurance(player, hand, hand_num)
                    hand = hand.next_hand
                    hand_num += 1
            
            if self.dealer.get_first_hand().is_blackjack():
                for player in self.players:
                    self._check_winner(player) 
                    
                self._ask_continue()
                return

        # Players' turns
        for player in self.players:
            if not player.in_game:
                continue

            hand = player.hands.hand
            hand_num = 1

            while hand:
                self._play_hand(player, hand, hand_num)
                hand = hand.next_hand
                hand_num += 1

        # Dealer draws until 17+
        dealer_hand = self.dealer.get_first_hand()

        while dealer_hand.calculate_card() < 17:
            dealer_hand.add_card(self.deck.card_deal())

        # Determine winners
        for player in self.players:
            if not player.in_game:
                    continue
            
            self._check_winner(player) 
            
        self._ask_continue()
        return
    
    def _initial_bet(self, player: Player) -> None:
        """Prompt the player to place an initial bet."""
        if player.balance < self.bet_manager.min_bet:
            raise ValueError(f"Insufficient funds. Minimum bet: {self.bet_manager.min_bet}")
        
        amount = self.ui.input_initial_bet(player, self.bet_manager)
        
        if self.bet_manager.bet(player, amount):
            return
    
    def _insurance(self, player: Player, hand: Hand, hand_num: int) -> None:
        """Offer insurance to the player."""
        while True:
            self.ui.show_hand(self.dealer, player, hand, hand_num)

            if not self.bet_manager.can_bet_for_insurance(player, hand):
                self.ui.show_cannot_buy_insurance(player, hand_num)
                return
            
            choice = self.ui.input_buy_insurance(hand.bet//2)

            if choice == "y":
                self.bet_manager.withdraw_insurance(player, hand)
                return
            elif choice == "n":
                return

    def _play_hand(self, player: Player, hand: Hand, hand_num: int) -> None:
        """Handle a single hand's turn."""
        if hand.calculate_card() == 21:
            self.ui.show_lable_blackjack()
            return
        
        can_bet_for_double_split = self.bet_manager.can_bet_for_split_double(player, hand)
        can_split = hand.can_split()
        bet = hand.bet
        double_txt = f", Double(d), for {bet}" if can_bet_for_double_split else ""
        split_txt = f", Split(1), for {bet}" if can_bet_for_double_split and can_split else ""

        while True:
            self.ui.show_hand(self.dealer, player, hand, hand_num, show_dealer=False)
            action = self.ui.input_play_hand(hand_num, double_txt, split_txt)

            if action == "h":
                hand.add_card(self.deck.card_deal())
                self._player_action(player, hand, hand_num)
                return
            elif action == "d" and double_txt:
                self.bet_manager.double_bet(player, hand)
                hand.add_card(self.deck.card_deal())
                self.ui.show_hand(self.dealer, player, hand, hand_num, show_dealer=False)
                return
            elif action == "1" and split_txt:
                if not can_split:
                    raise ValueError
                    
                self.bet_manager.withdraw_split(player, hand)
                split_hand = player.create_split_hand(hand)
                hand.add_card(self.deck.card_deal())
                split_hand.add_card(self.deck.card_deal())
                self._play_hand(player, hand, hand_num)
                return
            elif action.lower() == "s":
                return
            else:
                self.ui.show_invalid_hand_action()

    def _player_action(self, player: Player, hand: Hand, hand_num: int) -> None:
        """Hit/Stand loop for a hand."""
        self.ui.show_hand(self.dealer, player, hand, hand_num, show_dealer=False)

        while hand.calculate_card() <= 21:
            if hand.calculate_card() == 21:
                self.ui.show_have_21(player, hand_num)
                return

            action = self.ui.input_hit_or_stop()

            if action == "h":
                hand.add_card(self.deck.card_deal())
                self.ui.show_hand(self.dealer, player, hand, hand_num, show_dealer=False)
            elif action == "s":
                return       

    def _dealer_have_blackjack(self, player: Player, hand: Hand) -> None:
        """Handle case when dealer has blackjack."""
        if hand.insurance:
            self.bet_manager.deposit_insurance(player, hand)
        
        if hand.is_blackjack():
            self.bet_manager.resolve_main_bet(player, hand, False, tie=True)
            self.ui.show_both_blackjack()
        else:
            self.bet_manager.resolve_main_bet(player, hand, False)
            self.ui.show_lose_deaker_has_blackjack()

    def _check_winner(self, player: Player) -> None:
        """Evaluate all hands of a player against the dealer."""
        dealer_score = self.dealer.get_first_hand().calculate_card()
        self.ui.show_lable_final_res()
        hand = player.hands.hand
        hand_num = 1

        while hand:
            self.ui.show_hand(self.dealer, player, hand, hand_num, show_dealer=True)
            card_score = hand.calculate_card()

            if self.dealer.get_first_hand().is_blackjack():
                self._dealer_have_blackjack(player, hand)
            elif hand.is_blackjack():
                self.bet_manager.blackjack(player, hand)
            elif hand.insurance:
                self.ui.show_insurance_lose(hand.bet//2)
            else:
                self.ui.show_final_res(player.name, self.dealer.name, card_score, dealer_score)

                if card_score > 21:
                    self.ui.show_player_bust(player.name)
                    self.bet_manager.resolve_main_bet(player, hand, False)
                elif dealer_score > 21 or card_score > dealer_score:
                    self.bet_manager.resolve_main_bet(player, hand, True)    
                elif card_score < dealer_score:
                    self.bet_manager.resolve_main_bet(player, hand, False)
                else:
                    self.bet_manager.resolve_main_bet(player, hand, False, tie=True)
            
            hand = hand.next_hand
            hand_num += 1
        
        player.reset_hand()


    def _ask_continue(self) -> None:
        """Ask if players want to continue playing."""
        continue_game = self.ui.ask_continue()

        if continue_game == "y":
            self.start_game()
            return
        elif continue_game == "n":
            self.players = []
            return
    
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