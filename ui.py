from typing import List, Optional, Dict, Union

class ConsoleUI:
    """Console user interface for Blackjack game."""
    def start_message(self) -> None:
        """Display welcome message."""
        print("Welcome to Blackjack Casino!")
    
    def show_action_with_session(self) -> str:
        """Display session management menu."""
        while True:
            print("\nSelect action:")
            print("[0] Exit")
            print("[1] Create session")
            print("[2] Load session")
            print("[3] Delete session")
            choice = input("> ").strip().lower()

            if choice in ("0", "1", "2", "3",):
                return choice
            
            print("Invalid choice. Please try again.")
            
    def show_no_session(self) -> None:
        """Notify that no session is selected."""
        print("\nNo session selected.")
    
    def input_first_session_name(self) -> str:
        """Request session name for new session."""
        while True:
            print("\nEnter session name.")
            session_name = input("> ").strip()
            if session_name:
                return session_name
            
            print("Not empty string.")
    
    def input_session_name(self) -> str:
        """Request session name with cancel option."""
        print("\nEnter session name or 0 to exit.")
        session_name = input("> ").strip()
        return session_name

    def show_cancelled_session(self) -> None:
        """Notify session creation cancelled."""
        print("\nSession creation cancelled.")
    
    def show_session_create(self, session_name: str) -> None:
        """Notify successful session creation."""
        print(f"\nSession '{session_name}' created successfully.")
    
    def show_error_in_create_session(self, e: Exception) -> None:
        """Display error during session creation."""
        print(f"\nError: {e}")
        print("Please try again.")
    
    def show_choice_session(self, sessions: List[Dict]) -> int:
        """Display available sessions and get user choice."""
        while True:
            try:
                print("\nAvailable sessions:")

                for i, session in enumerate(sessions, 1):
                    print(f"[{i}] {session["name"]}, {session["last_played"]}")
                
                print(f"Select session (0 to cancel, 1-{len(sessions)}.)")
                choice = int(input(f"> "))

                if choice == 0:
                    print("Selection cancelled.")
                    return choice
                elif 0 < choice <= len(sessions):
                    return choice
                else:
                    print(f"Invalid choice. Please select 0 to {len(sessions)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def input_first_player_name(self) -> str:
        """Request first player's name."""
        print("\nEnter first player's name.")
        name = input("> ").strip()
        return name
    
    def show_defoult_player_name(self, players: List['Player']) -> None:
        """Notify default player created."""
        print("\nDefault player 'Player' created.")
    
    def input_new_player_name(self, players: List['Player']) -> str:
        """Request new player name with uniqueness validation."""
        while True:
            print("\nEnter new player's name (or 0 to cancel).")
            name = input("> ").strip()

            if name == "0":
                return name
            
            if not name:
                print("Name cannot be empty.")
                continue

            if any(p.name == name for p in players):
                print(f"Player '{name}' already exists.")
                return name
    
    def show_player_add(self, name: str) -> None:
        """Notify player added."""
        print(f"\nPlayer {name} added.")
    
    def show_menu(self, tables: Dict[str, 'BlackJack']) -> None:
        """Display a nicely formatted menu."""
        print("\n" + "┌" + "─" * 58 + "┐")
        print("│" + " " * 22 + "MAIN MENU" + " " * 27 + "│")
        print("├" + "─" * 58 + "┤")
        count = 1

        for key, table in tables.items():
            label = f"TABLE {key.upper()}"
            print(f"│ [{count}] {label:<11} │ {table.bet_manager.min_bet:>8}"\
                  f" – {table.bet_manager.max_bet:<8} │".ljust(59) + "│")
            count += 1

        print("├" + "─" * 58 + "┤")
        print("│ [4] ADD PLAYER" + " " * 43 + "│")
        print("│ [5] DEPOSIT BALANCE" + " " * 38 + "│")
        print("│ [6] REMOVE PLAYER" + " " * 40 + "│")
        print("├" + "─" * 58 + "┤")
        print("│ [0] EXIT" + " " * 49 + "│")
        print("└" + "─" * 58 + "┘")

    def input_choice_menu(self) -> str:
        """Get user menu choice."""
        print("\nYour choice:")
        choice = input("> ").strip()
        return choice
    
    def show_invalid_choice(self) -> None:
        """Notify invalid menu choice."""
        print("\nInvalid input. Choose 0-6.")
    
    def show_add_player_in_table(self, table: 'BlackJack', table_key: str) -> None:
        """Display table info when adding player."""
        print(f"\nPlaying at {table_key.upper()} table.")
        print(f"Limits: {table.bet_manager.min_bet} – {table.bet_manager.max_bet}.")

    def show_no_player_to_deposite(self):
        print("\nNo players to deposit.")
    
    def show_cannot_remove(self):
        print("\nCannot remove the only player.")
    
    def show_removed_player(self, player):
        print(f"\nPlayer {player.name} removed.")

    def show_player_list(self, players):
        print("\nPlayer list:")

        for i, p in enumerate(players):
            print(f"  [{i+1}] {p.name} ({p.balance})")
        print(f"  [{0}] Cancel.")

        while True:
            try:
                print("Select number: ")
                choice = int(input("> ")) - 1

                if -1 <= choice < len(players):
                    return choice
                
                print("Invalid number.")          
            except ValueError:
                print("Enter an integer.")
    
    def show_exit(self, players):
        """Exit the application and show final balances."""
        print("\nThank you for playing! Goodbye!")

        if players:
            print("\nFinal balances:")

            for p in players:
                print(f"  {p.name}: {p.balance}")
    
    def show_start_message_app_balance(self, amount):
        print(f"\n{amount} will be charged to your card.")

    def input_num_card(self):
        print("\nEnter card number (16 digits) or 0 to cancel")
        num_card = input("> ").strip()
        return num_card

    def show_num_card_error(self):
        print("Card number must be exactly 16 digits.\n")

    def input_card_date(self):
        print("\nEnter expiry date (MM/YY) or 0 to cancel.")
        date_card = input("> ").strip()
        return date_card
    
    def show_card_date_error(self):
        print("Date must be in format MM/YY (e.g., 12/25).")
    
    def input_cvv(self):
        print("\nEnter CVV (3 digits) or 0 to cancel.")
        cvv = input("\n> ").strip()
        return cvv

    def show_cvv_error(self):
        print("CVV must be 3 digits.")
    
    def show_finall_message_app_balance(self, player, amount):
        print(f"{player.name}'s balance increased by {amount}.")
    
    def show_min_bet(self, min_bet):
        print(f"\nMinimum bet is {min_bet}.")

    def show_max_bet(self, max_bet):
        print(f"\nMaximum bet is {max_bet}.")

    def enough_balance(self, balance):
        print(f"\nNot enough balance. You have {balance}.")
    
    def show_blackjack_win(self, name, win):
        print(f"{name}, blackjack! You win {win}.")
    
    def show_win(self, name, bet):
        print(f"{name} wins {bet}!")

    def show_tie(self, name, bet):
        print(f"{name}. push, bet returned {bet}.")

    def show_lose(self, name, bet):
        print(f"{name} loses {bet}.")
    
    def show_pushout_insurance(self, name, bet):
        print(f"{name}, insurance pays {bet}.")
    
    def show_cannot_play(self, player, min_bet):
        print(f"\n{player.name} cannot play: balance {player.balance} < min bet {min_bet}.")
    
    def input_add_hand(self, player):
        print(f"\n{player.name}, add another hand? (y/n).")
        choice = input("> ").strip().lower()

        if choice in ("y", "n"):
            return choice
        
        print("Please enter 'y' or 'n'.")
    
    def input_initial_bet(self, player, bet_manager):
        while True:
            try:
                print(f"\n{player.name} (balance {player.balance}) "
                                    f"Bet [{bet_manager.min_bet}..{bet_manager.max_bet}]: ")
                amount = int(input("> "))
                return amount
                
            except ValueError:
                print("Please enter an integer.")
    
    def show_cannot_buy_insurance(self, player, hand_num):
        print(f"\n{player.name}, hand {hand_num}: not enough money for insurance.")
    
    def input_buy_insurance(self, bet):
        print(f"\nBuy insurance for {bet}? (y/n).")
        choice = input(f"> ").strip().lower()

        if choice in ("y", "n"):
            return choice
        
        print("Enter 'y' or 'n'.")
    
    def show_lable_blackjack(self):
        print("\nBlackjack!")
    
    def input_play_hand(self, hand_num, double_txt, split_txt):
        while True:
            print(
                f"Hand {hand_num}:\n"
                f"Hit(h), Stand(s){double_txt}{split_txt}\n"
                "Your choice."
            )
            action = input("> ").strip().lower()
            return action

    def show_invalid_hand_action(self):
            print("\nInvalid input. Available: h, s, d, 1.\n")

    def show_have_21(self, player, hand_num):
        print(f"\n{player.name} (hand {hand_num}) have 21.")

    def input_hit_or_stop(self):
        while True:
            print("Hit(h) or Stand(s).")
            print("Your choice.")
            action = input("> ").strip().lower()

            if action in ("h", "s"):
                return action
            
            print("Enter 'h' or 's'.\n") 

    def show_hand(self, dealer, player, hand, hand_num: int, show_dealer: bool = False) -> None:
        """Display the player's hand and optionally the dealer's hand."""
        player_cards = hand.display_hand()
        player_score = hand.calculate_card()
        print(f"\n{player.name} (hand {hand_num}): {player_cards} | Score: {player_score}")
        dealer_hand = dealer.get_first_hand()

        if show_dealer:
            dealer_cards = dealer_hand.display_hand()
            dealer_score = dealer_hand.calculate_card()
            print(f"Dealer: {dealer_cards} | Score: {dealer_score}")
        else:
            first = str(dealer_hand.get_first_card()) if dealer_hand.cards else "??"
            print(f"Dealer: {first}, [hidden card]")

    def show_both_blackjack(self):
        print("Push (both have blackjack).")
    
    def show_lose_deaker_has_blackjack(self):
        print("Dealer has blackjack. You lose.")

    def show_lable_final_res(self):
        print("\nFinal results:")

    def show_insurance_lose(self, bet):
        print(f"\nInsurance lost (lost {bet}).")
    
    def show_final_res(self, player_name, dealer_name, player_score, dealer_score):
        print(f"{player_name} score: {player_score}")
        print(f"{dealer_name}'s score: {dealer_score}")
    
    def show_player_bust(self, name):
        print(f"{name} busted! Dealer win.")
    
    def show_player_win(self, name):
        print(f"{name} lose. Dealer win.")

    def show_player_lose(self, name):
        print(f"{name} lose. Dealer win.")
    
    def ask_continue(self):
        while True:
            print("\nPlay again? (y/n).")
            continue_game = input("> ").strip().lower()

            if continue_game == "y":
                return continue_game
            
            if continue_game == "n":
                print("\nThanks for playing!")
                return continue_game
            
            print("Enter 'y' or 'n'.")