from flask import Flask, render_template, request
from analytics import fetch_sessions_data, fetch_game_metadata, get_session_trends, get_longest_sessions, plot_trends, plot_heatmap, plot_calendar_heatmap, get_db_connection
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    db_path = os.getenv('DB_PATH', 'game_sessions.db')
    conn = get_db_connection(db_path)
    
    # Fetch all sessions data
    sessions_df = fetch_sessions_data(conn)

    # Handle date range filtering
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        sessions_df = sessions_df[(sessions_df['start_time'] >= start_date) & (sessions_df['start_time'] <= end_date)]
    
    trends = get_session_trends(sessions_df)
    plot_trends(trends)
    
    plot_heatmap(sessions_df)  # Generate the heatmap

    longest_sessions = get_longest_sessions(sessions_df)
    
    conn.close()

    return render_template('dashboard.html', trends_image='static/trends.png', heatmap_image='static/heatmap.png', longest_sessions=longest_sessions, start_date=start_date, end_date=end_date)

if __name__ == '__main__':
    app.run(debug=True)
