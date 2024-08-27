import datetime
import psutil
import logging
import json
import time
from database.sessions import create_sessions_table, log_session

class GameSessionTracker:
    def __init__(self, db_connection, games_file='games.json'):
        self.conn = db_connection
        self.cursor = self.conn.cursor()
        self.active_sessions = {}
        self.games_file = games_file
        self.games = self.load_games()

        create_sessions_table(self.cursor)

    def load_games(self):
        try:
            with open(self.games_file, 'r') as f:
                games = json.load(f)
            logging.info(f"Loaded games configuration: {games}")
            return games
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Failed to load games: {e}")
            return {}

    def track_game_sessions(self):
        try:
            logging.info("Started tracking game sessions.")
            print("Started tracking game sessions.")
            while True:
                self.check_running_games()
                self.check_closed_games()
                time.sleep(5)  # Check every 5 seconds
        except KeyboardInterrupt:
            logging.info("Stopping game session tracker...")
            print("Stopping game session tracker...")
        finally:
            self.close()

    def check_running_games(self):
        for process in psutil.process_iter(['pid', 'name']):
            exe_name = process.info['name']

            for game_name, game_exe in self.games.items():
                if exe_name.lower() == game_exe.lower() and game_exe not in self.active_sessions:
                    start_time = datetime.datetime.now()
                    self.active_sessions[game_exe] = start_time
                    logging.info(f"Started playing {game_name} at {start_time}")
                    print(f"Started playing {game_name} at {start_time}")

    def check_closed_games(self):
        for game_exe in list(self.active_sessions.keys()):
            if not any(p.info['name'].lower() == game_exe.lower() for p in psutil.process_iter(['name'])):
                start_time = self.active_sessions.pop(game_exe)
                end_time = datetime.datetime.now()
                duration = (end_time - start_time).total_seconds() / 60.0  # Duration in minutes
                game_name = next(key for key, value in self.games.items() if value.lower() == game_exe.lower())
                log_session(self.cursor, game_exe, game_name, start_time, end_time, duration)
                print(f"Stopped playing {game_name} at {end_time}. Duration: {duration:.2f} minutes.")

    def close(self):
        self.cursor.close()
        logging.info("Game session tracker closed.")
