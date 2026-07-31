import os
import sqlite3
from datetime import datetime
from typing import List, Dict

class SaveManager:
    """Singleton manager for database operations."""
    _instance = None
    _current_session_id = None

    def __new__(cls, db_file: str = "data/game.db"):
        if cls._instance is None:
            cls._instance = super(SaveManager, cls).__new__(cls)
            cls._instance._initialized = False

        return cls._instance

    def __init__(self, db_file: str = "data/game.db"):
        if self._initialized:
            return
        
        self._initialized = True
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self._init_db()
        self.conn.execute("PRAGMA foreign_keys = ON")

    def _init_db(self) -> None:
        """Initialize database tables and indexes."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TEXT NOT NULL,
                    last_played TEXT NOT NULL
                )
            """)

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    balance REAL NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
                    UNIQUE(session_id, name)
                )
            """)

            self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_players_session
                ON players(session_id)
            """)
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all sessions ordered by creation date."""
        cursor = self.conn.execute(
            "SELECT * FROM sessions ORDER BY created_at DESC"
        )
        return [dict(row) for row in cursor.fetchall()]

    def create_session(self, session_name: str) -> None:
        """Create a new session with current timestamp."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            with self.conn:
                cursor = self.conn.execute(
                    """
                    INSERT INTO sessions (name, created_at, last_played)
                    VALUES (?, ?, ?)
                    """,
                    (session_name, now, now)
                )
                session_id = cursor.lastrowid
                self._current_session_id = session_id
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"Session '{session_name}' already exists")

    def delete_session(self, session_id: int) -> None:
        """Delete a session by ID."""
        # Check if session exists
        with self.conn:
            session = self.conn.execute(
                "SELECT name FROM sessions WHERE id = ?", (session_id,)
            ).fetchone()
        
        if not session:
            raise ValueError

        # Delete the session
        with self.conn:
            self.conn.execute(
                "DELETE FROM sessions WHERE id = ?",
                (session_id,)
            )

        # Clear current session if deleted
        if self._current_session_id == session_id:
            self._current_session_id = None
    
    def add_player_in_session(self, player) -> None:
        """Add a player to the current session."""
        if not self._current_session_id:
            raise ValueError("Нет активной сессии")
        
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO players (session_id, name, balance) VALUES (?, ?, ?)",
                    (self._current_session_id, player.name, player.balance)
                )
                
            self._update_last_played(self._current_session_id)
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"Player '{player.name}' already exists in this session")
            
            raise
    
    def get_players_by_session(self, session_id: int) -> List[Dict]:
        """Get all players from a specific session."""
        with self.conn:
            players_data = self.conn.execute(
                "SELECT name, balance FROM players WHERE session_id = ?", (session_id,)
            ).fetchall()

        self._update_last_played(session_id)
        self._current_session_id = session_id
        return players_data

    def delete_player(self, player_name: str) -> None:
        """Delete a player from the current session."""
        # Check if player exists
        with self.conn:
            player = self.conn.execute(
                "SELECT id FROM players WHERE name = ? AND session_id = ?", (player_name, self._current_session_id)
            ).fetchone()
        
        if not player:
            raise ValueError
        
        player_id = player[0]

        # Delete the player
        with self.conn:
            self.conn.execute(
                "DELETE FROM players WHERE id = ? AND session_id = ?",
                (player_id, self._current_session_id)
            )

        self._update_last_played(self._current_session_id)

    def update_player_balance(self, player) -> None:
        """Update player's balance in current session."""
        with self.conn:
            result = self.conn.execute(
                    "UPDATE players SET balance = ? WHERE session_id = ? AND name = ?",
                    (player.balance, self._current_session_id, player.name)
                )
            
        self._update_last_played(self._current_session_id)
    
    def _update_last_played(self, session_id) -> None:
        """Update player's balance in current session."""
        with self.conn:
            self.conn.execute(
                    "UPDATE sessions SET last_played = ? WHERE id = ?",
                    (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), session_id)
                )

    def close(self) -> None:
        """Close the database connection."""
        if hasattr(self, 'conn'):
            self.conn.close()