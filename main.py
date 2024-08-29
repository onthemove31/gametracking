from modules.tracker import track_game_sessions
from modules.analytics import get_detailed_session_analytics, analyze_gaming_habits
from modules.game_progress import update_game_progress
from modules.recommendations import recommend_games_based_on_played
from database.connection import create_db_connection
import pandas as pd

def main():
    games = {
        "Cyberpunk 2077": "Cyberpunk2077.exe",
        "The Witcher 3": "witcher3.exe",
        "Diablo IV": "Diablo IV.exe",
        "Dota 2": "dota2.exe"
        # Add more games as needed
    }

    # Track game sessions
    track_game_sessions(games)

    # Perform analytics and recommendations after tracking
    conn = create_db_connection()
    df = pd.read_sql_query("SELECT * FROM sessions", conn)
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    analytics = get_detailed_session_analytics(df)
    late_night_percentage = analyze_gaming_habits(df)
    print(f"Percentage of late-night gaming: {late_night_percentage:.2f}%")
    
    recommendations = recommend_games_based_on_played(df)
    for rec in recommendations:
        print(f"Recommended Game: {rec['game_name']} - Developer: {rec.get('developer', 'N/A')} - Cover: {rec.get('cover_url', 'N/A')}")
    
    conn.close()

if __name__ == "__main__":
    main()
