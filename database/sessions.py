import sqlite3
import logging

def create_sessions_table(cursor):
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            exe_name TEXT NOT NULL,
                            game_name TEXT NOT NULL,
                            start_time TEXT NOT NULL,
                            end_time TEXT,
                            duration REAL)''')
        cursor.connection.commit()
        logging.info("Sessions table ensured in database.")
    except sqlite3.Error as e:
        logging.error(f"Failed to create table: {e}")
        raise

def log_session(cursor, exe_name, game_name, start_time, end_time, duration):
    try:
        cursor.execute('''INSERT INTO sessions (exe_name, game_name, start_time, end_time, duration)
                           VALUES (?, ?, ?, ?, ?)''',
                       (exe_name, game_name, start_time.strftime('%Y-%m-%d %H:%M:%S'),
                        end_time.strftime('%Y-%m-%d %H:%M:%S'), duration))
        cursor.connection.commit()
        logging.info(f"Logged session for {game_name}: {duration:.2f} minutes.")
    except sqlite3.Error as e:
        logging.error(f"Failed to log session: {e}")
        raise
