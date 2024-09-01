import psutil
import datetime
import time
import logging
from game_tracker.database import store_session
from game_tracker.game_identifier import custom_games
from game_tracker.telemetry_tracker import collect_telemetry, close_telemetry_db

logging.basicConfig(level=logging.INFO)

def track_game_sessions():
    active_sessions = {}

    while True:
        for exe_name, game_name in custom_games.items():
            # Check if the process is running
            if any(proc.info['name'].lower() == exe_name for proc in psutil.process_iter(['name'])):
                if exe_name not in active_sessions:
                    start_time = datetime.datetime.now()
                    active_sessions[exe_name] = start_time
                    logging.info(f"Started tracking {game_name} at {start_time}")
                # Collect telemetry data while the game is running
                collect_telemetry()
            else:
                # If the process is no longer running but was active, stop tracking
                if exe_name in active_sessions:
                    start_time = active_sessions.pop(exe_name)
                    end_time = datetime.datetime.now()
                    duration = (end_time - start_time).total_seconds() / 60.0
                    store_session(exe_name, game_name, start_time, end_time, duration)
                    logging.info(f"Stopped tracking {game_name}. Duration: {duration:.2f} minutes.")

        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    try:
        track_game_sessions()
    finally:
        close_telemetry_db()