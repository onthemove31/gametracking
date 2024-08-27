import unittest
from unittest.mock import patch, MagicMock
import os
import sqlite3
import json
import datetime  # Import datetime module
from game_session_tracker import GameSessionTracker  # Adjust the import according to your project structure

class TestGameSessionTracker(unittest.TestCase):

    @patch('game_session_tracker.psutil.process_iter')
    def test_check_running_games(self, mock_process_iter):
        tracker = GameSessionTracker()
        mock_process = MagicMock()
        mock_process.info = {'name': 'Cyberpunk2077.exe'}
        mock_process_iter.return_value = [mock_process]

        tracker.check_running_games()
        self.assertIn('Cyberpunk2077.exe', tracker.active_sessions)

    @patch('game_session_tracker.psutil.process_iter')
    def test_check_closed_games(self, mock_process_iter):
        tracker = GameSessionTracker()
        tracker.active_sessions['Cyberpunk2077.exe'] = datetime.datetime.now() - datetime.timedelta(minutes=30)
        
        mock_process_iter.return_value = []
        with patch.object(tracker, 'log_session') as mock_log_session:
            tracker.check_closed_games()
            mock_log_session.assert_called_once_with('Cyberpunk2077.exe')

    def test_load_games(self):
        tracker = GameSessionTracker()
        games = tracker.load_games()
        self.assertIn("Cyberpunk 2077", games)
        self.assertEqual(games["Cyberpunk 2077"], "Cyberpunk2077.exe")

    def test_connect_db(self):
        tracker = GameSessionTracker()
        tracker.connect_db()
        self.assertIsNotNone(tracker.conn)
        self.assertIsNotNone(tracker.cursor)
        tracker.close_db_connection()

    def test_create_sessions_table(self):
        tracker = GameSessionTracker()
        tracker.connect_db()
        tracker.create_sessions_table()
        tracker.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sessions';")
        self.assertEqual(tracker.cursor.fetchone()[0], 'sessions')
        tracker.close_db_connection()

if __name__ == '__main__':
    unittest.main()
