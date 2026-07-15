from game import Black_jack
from balance_manager import Deposit
from player import Player
from typing import Dict, Optional, List

class CasinoApp:
    """Main casino application – manages players and tables."""

    def __init__(self, initial_balance: int = 500) -> None:
        self.deposit = Deposit(initial_balance)

        # Tables with different limits
        self.tables: Dict[str, Black_jack] = {
            'low': Black_jack(10, 1000, 5),
            'mid': Black_jack(1000, 10000, 5),
            'high': Black_jack(10000, 100000, 5)
        }

        self.players: List[Player] = []
        self.current_player: Optional[Player] = None

    def run(self) -> None:
        """Start the application."""
        print("Welcome to Blackjack Casino!")
        self._add_first_player()
        self._main_menu()

    def _add_first_player(self) -> None:
        """Add the first player on startup."""
        name = input("Enter first player's name: ").strip()
        if name:
            player = Player(name)
        else:
            player = Player("Player")
            print("Default player 'Player' created.")
        self.players.append(player)
        self.current_player = player

    def _main_menu(self) -> None:
        """Main menu loop."""
        while True:
            self._show_menu()
            choice = input("\nYour choice: ").strip()
            if choice == "0":
                self._exit_app()
                break
            elif choice == "1":
                self._play_at_table('low')
            elif choice == "2":
                self._play_at_table('mid')
            elif choice == "3":
                self._play_at_table('high')
            elif choice == "4":
                self._add_player()
            elif choice == "5":
                self._deposit_balance()
            elif choice == "6":
                self._remove_player()
            else:
                print("Invalid input. Choose 0-6.")
                input("Press Enter to continue...")

    def _show_menu(self) -> None:
        """Display a nicely formatted menu."""
        print("\n" + "┌" + "─" * 58 + "┐")
        print("│" + " " * 22 + "MAIN MENU" + " " * 27 + "│")
        print("├" + "─" * 58 + "┤")
        count = 1

        for key, table in self.tables.items():
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

        if self.current_player:
            print(f"\nCurrent player: {self.current_player.name} | Balance: {self.current_player.balance}")

    def _play_at_table(self, table_key: str) -> None:
        """Start a game at the chosen table."""
        table = self.tables[table_key]
        for player in self.players:
            table.add_player(player)

        print(f"\nPlaying at {table_key.upper()} table")
        print(f"Limits: {table.bet_manager.min_bet} – {table.bet_manager.max_bet}")
        table.start_game()

    def _add_player(self) -> None:
        """Add a new player."""
        while True:
            name = input("Enter new player's name (or 0 to cancel): ").strip()
            if name == "0":
                return
            if not name:
                print("Name cannot be empty.")
                continue
            if any(p.name == name for p in self.players):
                print(f"Player '{name}' already exists.")
                continue
            player = Player(name)
            self.players.append(player)
            print(f"Player {name} added.")
            return

    def _deposit_balance(self) -> None:
        """Deposit money to a selected player."""
        if not self.players:
            print("No players to deposit.")
            return
        player = self._select_player()
        if player:
            self.deposit.deposit(player)

    def _remove_player(self) -> None:
        """Remove a player (cannot remove the last one)."""
        if len(self.players) <= 1:
            print("Cannot remove the only player.")
            return
        player = self._select_player()
        if player:
            self.players.remove(player)
            print(f"Player {player.name} removed.")
            if self.current_player == player:
                self.current_player = self.players[0] if self.players else None

    def _select_player(self) -> Optional[Player]:
        """Select a player from the list."""
        print("\nPlayer list:")
        for i, p in enumerate(self.players):
            print(f"  [{i}] {p.name} ({p.balance})")
        print(f"  [{len(self.players)}] Cancel")

        while True:
            try:
                choice = int(input("Select number: "))
                if 0 <= choice < len(self.players):
                    return self.players[choice]
                if choice == len(self.players):
                    return None
                print("Invalid number.")
            except ValueError:
                print("Enter an integer.")

    def _exit_app(self) -> None:
        """Exit the application and show final balances."""
        print("\nThank you for playing! Goodbye!")
        if self.players:
            print("\nFinal balances:")
            for p in self.players:
                print(f"  {p.name}: {p.balance}₽")


def main():
    casino = CasinoApp()
    casino.run()

if __name__ == "__main__":
    main()