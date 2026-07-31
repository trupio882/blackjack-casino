from game import BlackJack
from save_manager import SaveManager
from balance_manager import Deposit
from player import Player
from typing import Dict, Optional, List
from ui import ConsoleUI

class CasinoApp:
    """Main casino application – manages players and tables."""
    DB: SaveManager = SaveManager()
    ui: ConsoleUI = ConsoleUI()

    def __init__(self) -> None:
        self.deposit = Deposit(500)
        # Tables with different limits
        self.tables: Dict[str, BlackJack] = {
            'low': BlackJack(10, 1000, 5),
            'mid': BlackJack(1000, 10000, 5),
            'high': BlackJack(10000, 100000, 5)
        }
        self.players: List[Player] = []

    def run(self) -> None:
        """Start the application."""
        self.ui.start_message()

        if self.DB.get_all_sessions():
            if self._show_session():
                return
        else:
            self.create_first_session()

        self._main_menu()
   
    def _show_session(self) -> bool:
        """Show session management menu."""
        while True:
            res = self.ui.show_action_with_session()

            if res == "0":
                return True
            elif res == "1":
                self.create_session()
                return False
            elif res == "2":
                session = self._choice_session()

                if session is None:
                    continue

                session_id = session["id"]
                data = self.DB.get_players_by_session(session_id)
                players = [
                    Player(row["name"], int(row["balance"])) 
                    for row in data
                ]
                    
                if not players:
                    self._add_first_player()
                
                self.players = players
                return False
            elif res == "3":
                session = self._choice_session()

                if session is None:
                    continue

                session_id = session["id"]
                self.DB.delete_session(session_id)         
    
    def create_first_session(self) -> None:
        """Create first session when no sessions exist."""
        session_name = self.ui.input_first_session_name()
        self.DB.create_session(session_name)
        self._add_first_player()
    
    def create_session(self) -> None:
        """Create new session with name validation."""
        while True:
            session_name = self.ui.input_session_name()

            if session_name == "0":
                self.ui.show_cancelled_session()
                return

            try:
                self.DB.create_session(session_name)
                self.ui.show_session_create(session_name)
                break
            except ValueError as e:
                self.ui.show_error_in_create_session(e)
        
        self._add_first_player()
    
    def _choice_session(self) -> Optional[Dict]:
        """Select a session from available list."""
        sessions = self.DB.get_all_sessions()

        if not sessions:
            self.ui.show_no_session()
            self.create_first_session()
            return None
        
        choice = self.ui.show_choice_session(sessions)

        if choice == 0:
            return
        
        return sessions[choice-1]
        
    def _add_first_player(self) -> None:
        """Add the first player on startup."""
        name = self.ui.input_first_player_name()

        if name:
            player = Player(name)
        else:
            player = Player("Player")
            self.ui.show_defoult_player_name()

        self.DB.add_player_in_session(player)
        self.players.append(player)

    def _main_menu(self) -> None:
        """Main menu loop."""
        while True:
            self.ui.show_menu(self.tables)
            choice = self.ui.input_choice_menu()

            if choice == "0":
                self.ui.show_exit(self.players)
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
                self.ui.show_invalid_choice()

    def _play_at_table(self, table_key: str) -> None:
        """Start a game at the chosen table."""
        table = self.tables[table_key]
        table.players.clear()

        for player in self.players:
            table.add_player(player)

        self.ui.show_add_player_in_table(table, table_key)
        table.start_game()

    def _add_player(self) -> None:
        """Add a new player."""
        name = self.ui.input_new_player_name(self.players)
        player = Player(name)
        self.DB.add_player_in_session(player)
        self.players.append(player)
        self.ui.show_player_add(name)

    def _deposit_balance(self) -> None:
        """Deposit money to a selected player."""
        if not self.players:
            self.ui.show_no_player_to_deposite()
            return
        
        player = self._select_player()

        if player:
            self.deposit.deposit(player)

    def _remove_player(self) -> None:
        """Remove a player (cannot remove the last one)."""
        if len(self.players) <= 1:
            self.ui.show_cannot_remove()
            return
        
        player = self._select_player()

        if player:
            self.players.remove(player)
            self.DB.delete_player(player.name)
            self.ui.show_removed_player()

    def _select_player(self) -> Optional[Player]:
        choice = self.ui.show_player_list(self.players)

        if 0 <= choice < len(self.players):
            return self.players[choice]
        
        if choice == -1:
            return None       


def main():
    casino = CasinoApp()
    casino.run()

if __name__ == "__main__":
    main()