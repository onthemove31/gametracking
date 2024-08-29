import requests
import os
from dotenv import load_dotenv
from database.connection import create_db_connection

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

def fetch_game_metadata(game_name):
    url = 'https://api.igdb.com/v4/games'
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }
    data = f'search "{game_name}"; fields name, involved_companies.name, cover.url;'

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        game_metadata = response.json()
        print(f"Fetched metadata for {game_name}: {game_metadata}")  # Debugging output
        return game_metadata
    else:
        print(f"Failed to fetch metadata for {game_name}. Status code: {response.status_code}")
        return None

def recommend_games_based_on_played(df):
    recommendations = []
    for game_name in df['game_name'].unique():
        game_metadata = fetch_game_metadata(game_name)
        
        if not game_metadata or len(game_metadata) == 0:
            print(f"No metadata found for {game_name}, skipping...")
            continue
        
        first_game = game_metadata[0]
        game_developers = [company['name'] for company in first_game.get('involved_companies', [])]
        
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
                    
    unique_recommendations = {rec['game_name']: rec for rec in recommendations}.values()
    
    return list(unique_recommendations)

# Example usage:
if __name__ == "__main__":
    conn = create_db_connection()
    df = pd.read_sql_query("SELECT * FROM sessions", conn)
    recommendations = recommend_games_based_on_played(df)
    for rec in recommendations:
        print(f"Recommended Game: {rec['game_name']} - Developer: {rec.get('developer', 'N/A')} - Cover: {rec.get('cover_url', 'N/A')}")
    conn.close()
