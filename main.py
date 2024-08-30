from modules.tracker import track_game_sessions
from modules.analytics import get_detailed_session_analytics, analyze_gaming_habits
from modules.game_progress import update_game_progress
from modules.recommendations import recommend_games_based_on_played
from database.connection import create_db_connection
from pystray import Icon, MenuItem as Item, Menu
from PIL import Image, ImageDraw
import threading
import pandas as pd
import tkinter as tk
from tkinter import ttk

def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height), fill=color2)
    dc.rectangle((0, 0, width // 2, height), fill=color2)
    return image

def on_quit(icon, item):
    icon.stop()

def fetch_historical_sessions():
    conn = create_db_connection()
    df = pd.read_sql_query("SELECT * FROM sessions", conn)
    conn.close()

    if df.empty:
        return pd.DataFrame()

    # Convert start_time to datetime for easier manipulation
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    # Aggregate the data to show total time spent per game per day
    df['date'] = df['start_time'].dt.date
    aggregated_df = df.groupby(['date', 'game_name']).agg(total_time=('duration', 'sum')).reset_index()

    return aggregated_df.sort_values(by='date', ascending=False)

def show_historical_sessions(icon, item):
    data = fetch_historical_sessions()

    if data.empty:
        tk.messagebox.showinfo("Historical Sessions", "No historical data available.")
        return

    # Create a new Tkinter window
    root = tk.Tk()
    root.title("Historical Sessions")

    # Create a Treeview widget for displaying the table
    tree = ttk.Treeview(root, columns=("Date", "Game", "Total Time (minutes)"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Game", text="Game")
    tree.heading("Total Time (minutes)", text="Total Time (minutes)")

    # Insert the data into the treeview
    for _, row in data.iterrows():
        tree.insert("", "end", values=(row['date'], row['game_name'], f"{row['total_time']:.2f}"))

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Pack the Treeview
    tree.pack(fill="both", expand=True)

    root.mainloop()

def main():
    games = {
        "Cyberpunk 2077": "Cyberpunk2077.exe",
        "The Witcher 3": "witcher3.exe",
        "Diablo IV": "Diablo IV.exe",
        "Dota 2": "dota2.exe"
        # Add more games as needed
    }

    # Create the system tray icon
    image = create_image(64, 64, "black", "red")
    menu = Menu(
        Item("Check Historical Sessions", show_historical_sessions),
        Item("Quit", on_quit)
    )
    icon = Icon("game-tracker", image, "Game Tracker", menu)

    # Function to update the tooltip of the system tray icon
    def update_status(message):
        icon.title = message

    # Run the tracking logic in a separate thread
    tracking_thread = threading.Thread(target=track_game_sessions, args=(games, update_status), daemon=True)
    tracking_thread.start()

    # Run the system tray icon
    icon.run()

    # Perform analytics and recommendations after tracking
    conn = create_db_connection()
    df = pd.read_sql_query("SELECT * FROM sessions", conn)
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    # Analytics
    analytics = get_detailed_session_analytics(df)
    late_night_percentage = analyze_gaming_habits(df)
    print(f"Percentage of late-night gaming: {late_night_percentage:.2f}%")

    # Game Progress (Example usage)
    update_game_progress("Cyberpunk 2077", progress_percentage=75, achievements_unlocked=10, total_achievements=20)

    # Recommendations
    recommendations = recommend_games_based_on_played(df)
    for rec in recommendations:
        print(f"Recommended Game: {rec['game_name']} - Developer: {rec.get('developer', 'N/A')} - Cover: {rec.get('cover_url', 'N/A')}")
    
    conn.close()

if __name__ == "__main__":
    main()
