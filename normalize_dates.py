import sqlite3
from datetime import datetime

def normalize_dates_in_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, start_time, end_time FROM sessions")
    rows = cursor.fetchall()

    for row in rows:
        record_id = row[0]
        start_time = row[1]
        end_time = row[2]

        # Normalize start_time and end_time to a consistent format
        try:
            normalized_start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            normalized_start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        try:
            normalized_end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            normalized_end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        # Update the records in the database
        cursor.execute("""
            UPDATE sessions
            SET start_time = ?, end_time = ?
            WHERE id = ?
        """, (normalized_start_time, normalized_end_time, record_id))

    conn.commit()
    conn.close()

# Run the normalization
normalize_dates_in_db('game_sessions.db')
