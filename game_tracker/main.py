from game_tracker.game_tracker import track_game_sessions
from game_tracker.telemetry_tracker import track_telemetry

if __name__ == "__main__":
    track_game_sessions()
    # Example to start telemetry tracking for a specific game
    # track_telemetry("Cyberpunk2077.exe")
