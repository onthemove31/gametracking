import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        'DB_PATH': os.getenv('DB_PATH', 'game_sessions.db')
    }
