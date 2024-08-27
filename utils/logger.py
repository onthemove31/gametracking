import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='game_session_tracker.log', filemode='a')
    logging.info("Logging setup complete.")
