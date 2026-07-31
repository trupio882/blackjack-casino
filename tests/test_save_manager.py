import pytest
import sqlite3
import os
from save_manager import SaveManager
from player import Player

class TestSaveManager:
    @pytest.fixture
    def db_file(self, tmp_path):
        """Create a temporary database file."""
        db_path = tmp_path / "test_game.db"
        return str(db_path)

    @pytest.fixture
    def save_manager(self, db_file):
        """Create SaveManager instance with test database."""
        # Reset singleton for testing
        SaveManager._instance = None
        SaveManager._current_session_id = None
        return SaveManager(db_file)

    def test_singleton(self, db_file):
        sm1 = SaveManager(db_file)
        sm2 = SaveManager(db_file)
        assert sm1 is sm2

    def test_init_db_creates_tables(self, db_file):
        sm = SaveManager(db_file)
        
        # Check if tables were created
        cursor = sm.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('sessions', 'players')"
        )
        tables = cursor.fetchall()
        assert len(tables) == 2

    def test_create_session(self, save_manager):
        save_manager.create_session("TestSession")
        
        sessions = save_manager.get_all_sessions()
        assert len(sessions) == 1
        assert sessions[0]["name"] == "TestSession"

    def test_create_duplicate_session(self, save_manager):
        save_manager.create_session("TestSession")
        
        with pytest.raises(ValueError, match="Session 'TestSession' already exists"):
            save_manager.create_session("TestSession")

    def test_delete_session(self, save_manager):
        save_manager.create_session("TestSession")
        sessions = save_manager.get_all_sessions()
        session_id = sessions[0]["id"]
        
        save_manager.delete_session(session_id)
        sessions = save_manager.get_all_sessions()
        assert len(sessions) == 0

    def test_delete_nonexistent_session(self, save_manager):
        with pytest.raises(ValueError):
            save_manager.delete_session(999)

    def test_add_player_in_session(self, save_manager):
        save_manager.create_session("TestSession")
        player = Player("TestPlayer", 1000)
        
        save_manager.add_player_in_session(player)
        
        players = save_manager.get_players_by_session(
            SaveManager._current_session_id
        )
        assert len(players) == 1
        assert players[0]["name"] == "TestPlayer"
        assert players[0]["balance"] == 1000

    def test_add_player_without_session(self, save_manager):
        player = Player("TestPlayer", 1000)
        
        with pytest.raises(ValueError, match="Нет активной сессии"):
            save_manager.add_player_in_session(player)

    def test_get_players_by_session(self, save_manager):
        save_manager.create_session("TestSession")
        session_id = SaveManager._current_session_id
        
        player1 = Player("Player1", 1000)
        player2 = Player("Player2", 2000)
        save_manager.add_player_in_session(player1)
        save_manager.add_player_in_session(player2)
        
        players = save_manager.get_players_by_session(session_id)
        assert len(players) == 2
        assert players[0]["name"] == "Player1"
        assert players[1]["name"] == "Player2"

    def test_delete_player(self, save_manager):
        save_manager.create_session("TestSession")
        player = Player("TestPlayer", 1000)
        save_manager.add_player_in_session(player)
        
        save_manager.delete_player("TestPlayer")
        
        players = save_manager.get_players_by_session(
            SaveManager._current_session_id
        )
        assert len(players) == 0

    def test_update_player_balance(self, save_manager):
        save_manager.create_session("TestSession")
        player = Player("TestPlayer", 1000)
        save_manager.add_player_in_session(player)
        
        player.balance = 2500
        save_manager.update_player_balance(player)
        
        players = save_manager.get_players_by_session(
            SaveManager._current_session_id
        )
        assert players[0]["balance"] == 2500

    def test_close_connection(self, save_manager):
        save_manager.close()
        
        with pytest.raises(sqlite3.ProgrammingError):
            save_manager.conn.execute("SELECT 1")