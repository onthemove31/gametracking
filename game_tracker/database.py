from dotenv import load_dotenv
import os
import sqlite3

# Load environment variables from .env file
load_dotenv()

# Access environment variables
game_session_db_path = os.getenv('GAME_SESSION_DB_PATH')
telemetry_db_path = os.getenv('TELEMETRY_DB_PATH')

# Convert relative paths to absolute paths
game_session_db_path = os.path.abspath(game_session_db_path)
telemetry_db_path = os.path.abspath(telemetry_db_path)

# Check if the paths are correct
if not os.path.exists(os.path.dirname(game_session_db_path)):
    raise ValueError(f"Directory for GAME_SESSION_DB_PATH does not exist: {os.path.dirname(game_session_db_path)}")

if not os.path.exists(os.path.dirname(telemetry_db_path)):
    raise ValueError(f"Directory for TELEMETRY_DB_PATH does not exist: {os.path.dirname(telemetry_db_path)}")

# Database connection for game sessions
session_conn = sqlite3.connect(game_session_db_path)
session_cursor = session_conn.cursor()

# Create the sessions table if it doesn't exist
session_cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            exe_name TEXT NOT NULL,
                            game_name TEXT NOT NULL,
                            start_time TEXT NOT NULL,
                            end_time TEXT NOT NULL,
                            duration REAL)''')

def store_session(exe_name, game_name, start_time, end_time, duration):
    session_cursor.execute('''INSERT INTO sessions (exe_name, game_name, start_time, end_time, duration)
                              VALUES (?, ?, ?, ?, ?)''',
                           (exe_name, game_name, start_time.strftime('%Y-%m-%d %H:%M:%S'), 
                            end_time.strftime('%Y-%m-%d %H:%M:%S'), duration))
    session_conn.commit()

def close_databases():
    session_conn.close()
