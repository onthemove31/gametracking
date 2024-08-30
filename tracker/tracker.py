import time
import datetime
import psutil
import requests

# Define the games you want to track
games = {
    "Cyberpunk 2077": "Cyberpunk2077.exe",
    "The Witcher 3": "witcher3.exe",
    "Diablo IV": "Diablo IV.exe",
    "Dota 2": "dota2.exe",
    # Add more games as needed
}

# Function to send telemetry data to the Flask service
def send_telemetry(game_name, user_id, start_time, end_time, system_metrics, errors):
    telemetry_data = {
        "gameName": game_name,
        "userId": user_id,
        "startTime": start_time.isoformat(),
        "endTime": end_time.isoformat() if end_time else None,
        "systemMetrics": system_metrics,
        "errors": errors
    }
    
    try:
        response = requests.post("http://localhost:5000/track", json=telemetry_data)
        response.raise_for_status()
        print(f"Telemetry data sent successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send telemetry data: {e}")

# Function to track game sessions
def track_game_sessions():
    active_sessions = {}

    try:
        while True:
            # Check for running processes
            for process in psutil.process_iter(['pid', 'name']):
                exe_name = process.info['name']

                # Check if the process is one of the games
                for game_name, game_exe in games.items():
                    if exe_name.lower() == game_exe.lower():
                        if game_exe not in active_sessions:
                            start_time = datetime.datetime.now()
                            active_sessions[game_exe] = start_time
                            print(f"Started playing {game_name} at {start_time}")

                            # Capture initial system metrics
                            system_metrics = {
                                "cpu": psutil.cpu_percent(interval=1),
                                "memory": psutil.virtual_memory().used / (1024 * 1024)  # Memory usage in MB
                            }

                            # Send telemetry data when game starts
                            send_telemetry(game_name, "user123", start_time, None, system_metrics, None)

            # Check for games that have been closed
            for game_exe in list(active_sessions.keys()):
                if not any(p.info['name'].lower() == game_exe.lower() for p in psutil.process_iter(['name'])):
                    start_time = active_sessions.pop(game_exe)
                    end_time = datetime.datetime.now()

                    # Capture final system metrics
                    system_metrics = {
                        "cpu": psutil.cpu_percent(interval=1),
                        "memory": psutil.virtual_memory().used / (1024 * 1024)  # Memory usage in MB
                    }

                    # Send telemetry data when game ends
                    send_telemetry(next(key for key, value in games.items() if value.lower() == game_exe.lower()),
                                   "user123", start_time, end_time, system_metrics, None)

                    print(f"Stopped playing {game_name} at {end_time}. Duration: {(end_time - start_time).total_seconds() / 60:.2f} minutes.")

            time.sleep(5)  # Check every 5 seconds

    except KeyboardInterrupt:
        print("Stopping game session tracker...")

if __name__ == "__main__":
    track_game_sessions()
