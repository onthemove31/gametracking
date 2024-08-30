from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('telemetry_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create a new route for tracking telemetry data
@app.route('/track', methods=['POST'])
def track():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO telemetry_data (game_name, user_id, start_time, end_time, system_metrics, errors) VALUES (?, ?, ?, ?, ?, ?)",
                   (data['gameName'], data['userId'], data['startTime'], data['endTime'], str(data['systemMetrics']), data['errors']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Telemetry data saved successfully"}), 201

# Route to fetch telemetry data
@app.route('/telemetry', methods=['GET'])
def get_telemetry():
    conn = get_db_connection()
    telemetry_data = conn.execute('SELECT * FROM telemetry_data').fetchall()
    conn.close()

    telemetry_list = []
    for row in telemetry_data:
        telemetry_list.append({
            "id": row['id'],
            "game_name": row['game_name'],
            "user_id": row['user_id'],
            "start_time": row['start_time'],
            "end_time": row['end_time'],
            "system_metrics": row['system_metrics'],
            "errors": row['errors']
        })

    return jsonify(telemetry_list), 200

# Route to render the dashboard with graphs
@app.route('/')
def index():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM telemetry_data", conn)
    conn.close()

    if df.empty:
        return render_template('index.html', 
                               graph_most_played="No data available", 
                               graph_avg_duration="No data available", 
                               graph_cpu_usage="No data available", 
                               graph_memory_usage="No data available")

    # Handle different datetime formats including those with microseconds and with 'Z'
    df['start_time'] = pd.to_datetime(df['start_time'], utc=True, errors='coerce')
    df['end_time'] = pd.to_datetime(df['end_time'], utc=True, errors='coerce')

    # Calculate session duration
    df['session_duration'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60  # Duration in minutes
    average_duration = df.groupby('game_name')['session_duration'].mean()
    fig_avg_duration = px.bar(average_duration, x=average_duration.index, y=average_duration.values, 
                              labels={'x': 'Game', 'y': 'Average Duration (minutes)'}, title="Average Session Duration")
    graph_avg_duration = pio.to_html(fig_avg_duration, full_html=False)

    # Most Played Games
    most_played = df['game_name'].value_counts()
    fig_most_played = px.bar(most_played, x=most_played.index, y=most_played.values, 
                             labels={'x': 'Game', 'y': 'Number of Sessions'}, title="Most Played Games")
    graph_most_played = pio.to_html(fig_most_played, full_html=False)

    # System Performance Metrics
    df['cpu_usage'] = df['system_metrics'].apply(lambda x: eval(x)['cpu'])
    df['memory_usage'] = df['system_metrics'].apply(lambda x: eval(x)['memory'])

    average_cpu_usage = df.groupby('game_name')['cpu_usage'].mean()
    fig_cpu_usage = px.bar(average_cpu_usage, x=average_cpu_usage.index, y=average_cpu_usage.values, 
                           labels={'x': 'Game', 'y': 'Average CPU Usage (%)'}, title="Average CPU Usage")
    graph_cpu_usage = pio.to_html(fig_cpu_usage, full_html=False)

    average_memory_usage = df.groupby('game_name')['memory_usage'].mean()
    fig_memory_usage = px.bar(average_memory_usage, x=average_memory_usage.index, y=average_memory_usage.values, 
                              labels={'x': 'Game', 'y': 'Average Memory Usage (MB)'}, title="Average Memory Usage")
    graph_memory_usage = pio.to_html(fig_memory_usage, full_html=False)

    return render_template('index.html', 
                           graph_most_played=graph_most_played, 
                           graph_avg_duration=graph_avg_duration, 
                           graph_cpu_usage=graph_cpu_usage, 
                           graph_memory_usage=graph_memory_usage)

if __name__ == '__main__':
    app.run(debug=True)
