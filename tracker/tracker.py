import datetime
import psutil
import time
import os
import json  # Add this to handle JSON files
import requests
from dotenv import load_dotenv
from tracker.metadata import GameMetadataFetcher
from database.sessions import create_sessions_table, log_session
from database.backup import backup_database, restore_database

class GameSessionTracker:
    def __init__(self, db_connection, games_file='games.json'):
        load_dotenv()  # Load environment variables from .env file

        self.conn = db_connection
        self.cursor = self.conn.cursor()
        self.active_sessions = {}
        self.db_path = 'game_sessions.db'
        self.backup_dir = 'backups'
        self.games_file = games_file
        self.games = self.load_games()  # Initialize the games attribute

        self.client_id = os.getenv('IGDB_CLIENT_ID')
        self.access_token = self.get_access_token()
        self.metadata_fetcher = GameMetadataFetcher(client_id=self.client_id, access_token=self.access_token)

        create_sessions_table(self.cursor)

    def load_games(self):
        # Load the games from the JSON file
        if os.path.exists(self.games_file):
            with open(self.games_file, 'r') as f:
                return json.load(f)
        else:
            print(f"Games file {self.games_file} not found.")
            return {}

    def get_access_token(self):
        client_secret = os.getenv('IGDB_CLIENT_SECRET')
        token_url = 'https://id.twitch.tv/oauth2/token'
        data = {
            'client_id': self.client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }

        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print("Failed to obtain access token.")
            return None

    def track_game_sessions(self):
        # Automatically back up the database before starting
        backup_database(self.db_path, self.backup_dir)

        try:
            while True:
                self.check_running_games()
                self.check_closed_games()
                time.sleep(5)  # Check every 5 seconds
        except KeyboardInterrupt:
            print("Stopping game session tracker...")
        finally:
            self.close()

    def get_detailed_session_analytics(df):
        # Calculate session distribution by time of day
        df['hour'] = df['start_time'].dt.hour
        session_distribution = df.groupby('hour')['duration'].sum().sort_values(ascending=False)

        # Calculate weekly or monthly trends
        df['week'] = df['start_time'].dt.isocalendar().week
        weekly_trends = df.groupby('week')['duration'].sum().sort_values(ascending=False)

        # Add more detailed analysis as needed
        return session_distribution, weekly_trends

    def analyze_gaming_habits(df):
        # Example: Detect late-night gaming habits
        df['hour'] = df['start_time'].dt.hour
        late_night_sessions = df[(df['hour'] >= 22) | (df['hour'] <= 6)]
        
        total_late_night_hours = late_night_sessions['duration'].sum()
        total_hours = df['duration'].sum()
        
        percentage_late_night = (total_late_night_hours / total_hours) * 100

        # Suggest a break if necessary
        if percentage_late_night > 20:  # Example threshold
            print("Consider taking breaks during late-night gaming sessions.")
        
        return percentage_late_night
    
    # Function to recommend similar games
    def recommend_games_based_on_played(df, metadata_df):
        recommendations = []
        for game_name in df['game_name'].unique():
            game_metadata = fetch_game_metadata(game_name)
            if game_metadata:
                game_genres = game_metadata[0].get('genres', [])
                game_developers = [company['name'] for company in game_metadata[0].get('involved_companies', [])]
                
                for genre in game_genres:
                    data = f'fields name, genres, cover.url; where genres = ({genre}); limit 5;'
                    response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=data)
                    similar_games = response.json()
                    for similar_game in similar_games:
                        recommendations.append({
                            'game_name': similar_game['name'],
                            'genre': genre,
                            'cover_url': similar_game['cover']['url'] if 'cover' in similar_game else None
                        })

                for developer in game_developers:
                    data = f'fields name, involved_companies.name, cover.url; where involved_companies.name = "{developer}"; limit 5;'
                    response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=data)
                    similar_games = response.json()
                    for similar_game in similar_games:
                        recommendations.append({
                            'game_name': similar_game['name'],
                            'developer': developer,
                            'cover_url': similar_game['cover']['url'] if 'cover' in similar_game else None
                        })
                        
        # Removing duplicates
        unique_recommendations = {rec['game_name']: rec for rec in recommendations}.values()
        
        return list(unique_recommendations)


    def check_running_games(self):
        for process in psutil.process_iter(['pid', 'name']):
            exe_name = process.info['name']

            for game_name, game_exe in self.games.items():
                if exe_name.lower() == game_exe.lower() and game_exe not in self.active_sessions:
                    start_time = datetime.datetime.now()
                    self.active_sessions[game_exe] = start_time
                    print(f"Started playing {game_name} at {start_time}")

                    # Fetch and save metadata if it's a new game
                    metadata = self.metadata_fetcher.fetch_metadata(game_name)
                    if metadata:
                        self.metadata_fetcher.save_metadata(game_name, metadata, self.conn)

    def check_closed_games(self):
        for game_exe in list(self.active_sessions.keys()):
            if not any(p.info['name'].lower() == game_exe.lower() for p in psutil.process_iter(['name'])):
                start_time = self.active_sessions.pop(game_exe)
                end_time = datetime.datetime.now()
                duration = (end_time - start_time).total_seconds() / 60.0  # Duration in minutes
                game_name = next(key for key, value in self.games.items() if value.lower() == game_exe.lower())

                log_session(self.cursor, game_exe, game_name, start_time, end_time, duration)
                print(f"Stopped playing {game_name} at {end_time}. Duration: {duration:.2f} minutes.")

    def restore_from_backup(self, backup_filename):
        backup_path = os.path.join(self.backup_dir, backup_filename)
        restore_database(backup_path, self.db_path)

    def close(self):
        self.cursor.close()
        print("Database connection closed.")