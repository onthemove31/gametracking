# Game Session Tracker

The Game Session Tracker is a Python-based application that tracks the time you spend playing various games on your PC. It monitors running processes, logs the start and end times of gaming sessions, and stores the data in an SQLite database for later analysis.

## Features

- **Automatic Game Tracking**: Automatically tracks games based on their executable names.
- **Session Logging**: Logs the start and end times of each game session along with the duration.
- **SQLite Database Storage**: Stores session data in an SQLite database.
- **Configurable**: Uses a `.env` file for configuration and a JSON file for game executables.
- **Logging**: Logs application events to a log file for debugging and auditing.
- **Unit Tests**: Includes unit tests for critical components of the application.

## Project Structure

game_session_tracker/ │ ├── config/ │ ├── init.py │ └── settings.py ├── database/ │ ├── init.py │ ├── connection.py │ └── sessions.py ├── tracker/ │ ├── init.py │ └── tracker.py ├── utils/ │ ├── init.py │ └── logger.py ├── tests/ │ ├── init.py │ ├── test_tracker.py │ ├── test_connection.py │ └── test_sessions.py ├── main.py ├── .env ├── games.json ├── requirements.txt └── README.md


## Installation

### Prerequisites

- Python 3.7 or later
- SQLite (usually included with Python)

### Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/game-session-tracker.git
   cd game-session-tracker

2. **Set up a virtual environment (optional but recommended):**

       ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install dependencies:**

       ```bash
    pip install -r requirements.txt

4. **Configure your games:**

    Update the games.json file in the root directory with the executable names of the games you want to track:
   ```bash
    {
    "Cyberpunk 2077": "Cyberpunk2077.exe",
    "The Witcher 3": "witcher3.exe",
    "Diablo IV": "Diablo IV.exe",
    "Dota 2": "dota2.exe"
    }

5. **Usage**

    1. **Start the application:**

        Run the main program to start tracking your gaming sessions:

        ```bash
        python main.py
    
    2. **Check logs:**

        All application events, including session starts and stops, are logged in the game_session_tracker.log file.

    3. **Database:**

        The session data is stored in the SQLite database specified in the .env file (game_sessions.db by default).

6. **Running Tests**

    To run the unit tests, use the following command:

    ```bash
    python -m unittest discover -s tests

    This will execute all unit tests located in the tests directory.

7. **License**

    This project is licensed under the MIT License. See the LICENSE file for more details.


### How to Use This `README.md`
1. **Place the File**: Save the content as `README.md` in the root directory of your project.
2. **Push to GitHub**: Once the file is in place, it will be included in your next commit, and GitHub will automatically display it on your repository's main page.

This `README.md` will give users and contributors clear instructions on how to set up, use, and contribute to your project.






All application events, including session starts and stops, are logged in the game_session_tracker.log file.

Database:

The session data is stored in the SQLite database specified in the .env file (game_sessions.db by default).

Running Tests
To run the unit tests, use the following command:

bash
Copy code
python -m unittest discover -s tests
This will execute all unit tests located in the tests directory.

Contributing
Feel free to fork this repository and submit pull requests. Contributions are welcome!

License
This project is licensed under the MIT License. See the LICENSE file for more details.

vbnet
Copy code

### How to Use This `README.md`
1. **Place the File**: Save the content as `README.md` in the root directory of your project.
2. **Push to GitHub**: Once the file is in place, it will be included in your next commit, and GitHub will automatically display it on your repository's main page.

This `README.md` will give users and contributors clear instructions on how to set up, use, and contribute to your project.
