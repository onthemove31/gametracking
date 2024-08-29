import psutil
import time
from datetime import datetime
from database.connection import create_db_connection

def track_game_sessions(games):
    conn = create_db_connection()
    cursor = conn.cursor()

    active_sessions = {}

    try:
        while True:
            for process in psutil.process_iter(['pid', 'name']):
                exe_name = process.info['name']

                for game_name, game_exe in games.items():
                    if exe_name.lower() == game_exe.lower():
                        if game_exe not in active_sessions:
                            start_time = datetime.now()
                            active_sessions[game_exe] = start_time

            for game_exe in list(active_sessions.keys()):
                if not any(p.info['name'].lower() == game_exe.lower() for p in psutil.process_iter(['name'])):
                    start_time = active_sessions.pop(game_exe)
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds() / 60.0

                    cursor.execute('''INSERT INTO sessions (exe_name, game_name, start_time, end_time, duration)
                                      VALUES (?, ?, ?, ?, ?)''',
                                   (game_exe, game_name, start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                    end_time.strftime('%Y-%m-%d %H:%M:%S'), duration))
                    conn.commit()

            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping game session tracker...")
    finally:
        conn.close()

# Example usage in main.py or a dedicated function:
if __name__ == "__main__":
    games = {
        "Cyberpunk 2077": "Cyberpunk2077.exe",
        "The Witcher 3": "witcher3.exe",
        "Diablo IV": "Diablo IV.exe",
        "Dota 2": "dota2.exe"
        # Add more games as needed
    }
    track_game_sessions(games)
