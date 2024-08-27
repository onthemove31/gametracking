from tracker.tracker import GameSessionTracker
from utils.logger import setup_logging
from database.connection import create_db_connection
from config.settings import load_config

def main():
    setup_logging()
    config = load_config()
    db_connection = create_db_connection(config['DB_PATH'])

    tracker = GameSessionTracker(db_connection)
    tracker.track_game_sessions()

if __name__ == "__main__":
    main()
