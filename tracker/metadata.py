import requests
import os
import json
import sqlite3

class GameMetadataFetcher:
    def __init__(self, client_id, access_token):
        self.client_id = client_id
        self.access_token = access_token
        self.api_url = "https://api.igdb.com/v4/games"
        self.headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        }

    def fetch_metadata(self, game_name):
        search_query = f'search "{game_name}"; fields name,cover.url,summary,first_release_date;'
        response = requests.post(self.api_url, headers=self.headers, data=search_query)

        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]  # Return the first match
            else:
                print(f"No metadata found for {game_name}.")
                return None
        else:
            print(f"Failed to fetch metadata for {game_name}. Status Code: {response.status_code}")
            return None

    def save_metadata(self, game_name, metadata, db_connection):
        cursor = db_connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS game_metadata (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            game_name TEXT,
                            cover_url TEXT,
                            description TEXT,
                            release_date TEXT)''')

        cursor.execute('''INSERT INTO game_metadata (game_name, cover_url, description, release_date)
                          VALUES (?, ?, ?, ?)''', 
                          (game_name, 
                           metadata.get("cover", {}).get("url", ""),
                           metadata.get("summary", ""),
                           metadata.get("first_release_date", "")))

        db_connection.commit()
        print(f"Metadata for {game_name} saved.")
