import psutil
import time
from datetime import datetime
import sqlite3
import os
from pystray import Icon, MenuItem as Item, Menu
from PIL import Image, ImageDraw
import threading

def create_db_connection():
    db_path = os.getenv('DB_PATH', 'database/game_sessions.db')
    conn = sqlite3.connect(db_path)
    return conn

def track_game_sessions(games, update_status):
    conn = create_db_connection()
    cursor = conn.cursor()

    active_sessions = {}
    current_game = None

    try:
        while True:
            for process in psutil.process_iter(['pid', 'name']):
                exe_name = process.info['name']

                for game_name, game_exe in games.items():
                    if exe_name.lower() == game_exe.lower():
                        if game_exe not in active_sessions:
                            start_time = datetime.now()
                            active_sessions[game_exe] = start_time
                            current_game = game_name
                            update_status(f"Tracking {game_name}...")

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

                    current_game = None
                    update_status(f"Last tracked: {game_name} for {duration:.2f} minutes")

            if not current_game:
                update_status("No game is currently being tracked.")

            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping game session tracker...")
    finally:
        conn.close()

# System tray icon creation
def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height), fill=color2)
    dc.rectangle((0, 0, width // 2, height), fill=color2)
    return image

def on_quit(icon, item):
    icon.stop()

def main():
    games = {
        "Cyberpunk 2077": "Cyberpunk2077.exe",
        "The Witcher 3": "witcher3.exe",
        "Diablo IV": "Diablo IV.exe",
        "Dota 2": "dota2.exe"
        # Add more games as needed
    }

    # Create the system tray icon
    image = create_image(64, 64, "black", "red")
    menu = Menu(
        Item("Quit", on_quit)
    )
    icon = Icon("game-tracker", image, "Game Tracker", menu)

    # Function to update the tooltip of the system tray icon
    def update_status(message):
        icon.title = message

    # Run the tracking logic in a separate thread
    tracking_thread = threading.Thread(target=track_game_sessions, args=(games, update_status), daemon=True)
    tracking_thread.start()

    # Run the system tray icon
    icon.run()

if __name__ == "__main__":
    main()
