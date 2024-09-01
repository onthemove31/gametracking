from game_tracker.game_tracker import track_game_sessions
from game_tracker.telemetry_tracker import collect_telemetry, close_telemetry_db

def main():
    print("Starting game tracking...")
    try:
        track_game_sessions()
    finally:
        # Ensure the telemetry database connection is closed properly
        close_telemetry_db()

if __name__ == "__main__":
    main()
