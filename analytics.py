import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def get_db_connection(db_path='game_sessions.db'):
    return sqlite3.connect(db_path)

def fetch_sessions_data(conn):
    query = "SELECT * FROM sessions"
    df = pd.read_sql(query, conn)
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    df['duration'] = (df['duration'] / 60).round(2)  # Convert duration to hours and round to 2 decimal places
    
    # Debugging: Print a sample of the data to verify
    print("Fetched session data (in hours):\n", df.head())
    
    return df

def fetch_game_metadata(conn):
    query = "SELECT * FROM game_metadata"
    df = pd.read_sql(query, conn)
    df['release_date'] = pd.to_datetime(df['release_date'], unit='s').dt.strftime('%d/%m/%Y')  # Format release date
    
    # Debugging: Print a sample of the metadata to verify
    print("Fetched game metadata:\n", df.head())
    
    return df

def get_session_trends(df):
    df['day_name'] = df['start_time'].dt.day_name()  # Extract the day of the week
    trends = df.groupby('day_name')['duration'].sum().round(2)  # Group by day name and sum durations
    
    # Reindex to ensure all days are included, even if they have no data
    trends = trends.reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], fill_value=0)
    
    # Debugging: Print the trends data to verify
    print("Session trends by day of the week (in hours):\n", trends)
    
    return trends

def plot_trends(trends):
    plt.figure(figsize=(10, 6))
    trends.plot(kind='bar', color='blue')
    plt.title('Gaming Session Trends by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Total Duration (Hours)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('static/trends.png')
    plt.close()

def get_longest_sessions(df, top_n=5):
    # Group by game and find the longest session for each game
    df_grouped = df.groupby('game_name').apply(lambda x: x.nlargest(1, 'duration')).reset_index(drop=True)
    
    # Sort by duration and take the top N longest sessions
    df_grouped = df_grouped.sort_values('duration', ascending=False).head(top_n)
    
    # Debugging: Print the grouped sessions to verify
    print("Grouped longest sessions (in hours):\n", df_grouped[['game_name', 'duration', 'start_time']])
    
    return df_grouped


def plot_heatmap(df):
    df['hour'] = df['start_time'].dt.hour
    df['day_name'] = df['start_time'].dt.day_name()
    heatmap_data = df.pivot_table(index='hour', columns='day_name', values='duration', aggfunc='sum').fillna(0)
    
    # Reorder columns to reflect days of the week and ensure all days are included
    heatmap_data = heatmap_data.reindex(columns=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], fill_value=0)
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt=".2f", linewidths=.5, cbar=False, mask=(heatmap_data == 0), center=0)
    plt.title('Heatmap of Gaming Activity by Hour and Day (in Hours)')
    plt.xlabel('Day of the Week')
    plt.ylabel('Hour of the Day')
    plt.tight_layout()
    plt.savefig('static/heatmap.png')
    plt.close()

def plot_calendar_heatmap(df):
    # Create new columns for day of the week and the month
    df['day_of_week'] = df['start_time'].dt.weekday  # Monday=0, Sunday=6
    df['week_of_year'] = df['start_time'].dt.isocalendar().week
    df['month'] = df['start_time'].dt.month

    # Group the data by week, day, and sum the duration
    heatmap_data = df.groupby(['week_of_year', 'day_of_week'])['duration'].sum().unstack(fill_value=0)

    # Prepare the plot
    plt.figure(figsize=(15, 8))
    ax = plt.gca()

    # Plot circles
    for week in heatmap_data.index:
        for day in heatmap_data.columns:
            size = heatmap_data.loc[week, day]
            if size > 0:
                ax.scatter(day, week, s=size * 50, color='blue', alpha=0.6, edgecolor='black')  # Adjust the multiplier for circle size

    # Set labels and titles
    ax.set_xticks(range(7))
    ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    ax.set_yticks(range(heatmap_data.index.min(), heatmap_data.index.max() + 1))
    ax.set_yticklabels(heatmap_data.index)
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Week of the Year')
    ax.set_title('Gaming Activity Calendar Heatmap')

    plt.grid(False)
    plt.tight_layout()
    plt.savefig('static/calendar_heatmap.png')
    plt.close()