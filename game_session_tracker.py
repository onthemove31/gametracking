import sqlite3
import time
import datetime
import psutil
import os
import json
import logging
from dotenv import load_dotenv

class GameSessionTracker:
    def __init__(self):
        load_dotenv()
        self.db_path = os.getenv('DB_PATH', 'game_sessions.db')
        self.conn = None
        self.cursor = None
        self.active_sessions = {}

        self.games = self.load_games()

    def load_games(self):
        """Load the games list from a JSON file."""
        try:
            with open('games.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Failed to load games: {e}")
            return {}

    def connect_db(self):
        """Establish a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.create_sessions_table()
        except sqlite3.Error as e:
            logging.error(f"Database connection failed: {e}")
            raise

    def create_sessions_table(self):
        """Create the sessions table if it doesn't exist."""
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    exe_name TEXT NOT NULL,
                                    game_name TEXT NOT NULL,
                                    start_time TEXT NOT NULL,
                                    end_time TEXT,
                                    duration REAL)''')
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Failed to create table: {e}")
            raise

    def track_game_sessions(self):
        """Track game sessions by monitoring running processes."""
        try:
            while True:
                self.check_running_games()
                self.check_closed_games()
                time.sleep(5)  # Check every 5 seconds
        except KeyboardInterrupt:
            logging.info("Stopping game session tracker...")
        finally:
            self.close_db_connection()

    def check_running_games(self):
        """Check if any of the games have started."""
        for process in psutil.process_iter(['pid', 'name']):
            exe_name = process.info['name']

            for game_name, game_exe in self.games.items():
                if exe_name.lower() == game_exe.lower() and game_exe not in self.active_sessions:
                    start_time = datetime.datetime.now()
                    self.active_sessions[game_exe] = start_time
                    logging.info(f"Started playing {game_name} at {start_time}")

    def check_closed_games(self):
        """Check if any of the games have been closed."""
        for game_exe in list(self.active_sessions.keys()):
            if not any(p.info['name'].lower() == game_exe.lower() for p in psutil.process_iter(['name'])):
                self.log_session(game_exe)

    def log_session(self, game_exe):
        """Log the game session to the database."""
        start_time = self.active_sessions.pop(game_exe)
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds() / 60.0  # Duration in minutes
        game_name = next(key for key, value in self.games.items() if value.lower() == game_exe.lower())

        try:
            self.cursor.execute('''INSERT INTO sessions (exe_name, game_name, start_time, end_time, duration)
                                   VALUES (?, ?, ?, ?, ?)''',
                                (game_exe, game_name, start_time.strftime('%Y-%m-%d %H:%M:%S'), 
                                 end_time.strftime('%Y-%m-%d %H:%M:%S'), duration))
            self.conn.commit()
            logging.info(f"Stopped playing {game_name} at {end_time}. Duration: {duration:.2f} minutes.")
        except sqlite3.Error as e:
            logging.error(f"Failed to log session: {e}")
            raise

    def close_db_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    tracker = GameSessionTracker()
    tracker.connect_db()
    tracker.track_game_sessions()
