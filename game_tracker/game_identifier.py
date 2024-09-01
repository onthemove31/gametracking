import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the custom games from the JSON file
def load_custom_games():
    try:
        with open('games.json', 'r') as file:
            data = json.load(file)
        logging.info("Custom games loaded successfully.")
        return {game['exe_name'].lower(): game['name'] for game in data['games']}
    except FileNotFoundError:
        logging.error("games.json file not found. Please ensure the file exists.")
        return {}
    except json.JSONDecodeError:
        logging.error("Error decoding games.json. Please check the file format.")
        return {}

custom_games = load_custom_games()

def get_game_name_from_custom_games(exe_name):
    return custom_games.get(exe_name.lower())
