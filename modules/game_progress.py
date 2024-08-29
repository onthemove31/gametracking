from datetime import datetime
from database.connection import create_db_connection

def update_game_progress(game_name, progress_percentage=None, achievements_unlocked=None, total_achievements=None):
    conn = create_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO game_progress (game_name, progress_percentage, achievements_unlocked, total_achievements, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(game_name) DO UPDATE SET
            progress_percentage=COALESCE(?, progress_percentage),
            achievements_unlocked=COALESCE(?, achievements_unlocked),
            total_achievements=COALESCE(?, total_achievements),
            updated_at=CURRENT_TIMESTAMP
    ''', (game_name, progress_percentage, achievements_unlocked, total_achievements, datetime.now(),
          progress_percentage, achievements_unlocked, total_achievements, game_name))
    
    conn.commit()
    conn.close()

# Example usage:
if __name__ == "__main__":
    update_game_progress("Cyberpunk 2077", progress_percentage=75, achievements_unlocked=10, total_achievements=20)
