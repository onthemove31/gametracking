import unittest
from unittest.mock import patch, MagicMock
from tracker.tracker import GameSessionTracker
import datetime
import json

class TestGameSessionTracker(unittest.TestCase):

    @patch('tracker.tracker.psutil.process_iter')
    def test_check_running_games(self, mock_process_iter):
        mock_process = MagicMock()
        mock_process.info = {'name': 'Cyberpunk2077.exe'}
        mock_process_iter.return_value = [mock_process]

        mock_connection = MagicMock()
        tracker = GameSessionTracker(mock_connection)
        tracker.games = {"Cyberpunk 2077": "Cyberpunk2077.exe"}

        tracker.check_running_games()
        self.assertIn('Cyberpunk2077.exe', tracker.active_sessions)

    @patch('tracker.tracker.psutil.process_iter')
    @patch('tracker.tracker.log_session')  # Correctly patch the standalone function
    def test_check_closed_games(self, mock_log_session, mock_process_iter):
        mock_connection = MagicMock()
        tracker = GameSessionTracker(mock_connection)
        tracker.games = {"Cyberpunk 2077": "Cyberpunk2077.exe"}
        tracker.active_sessions['Cyberpunk2077.exe'] = datetime.datetime.now() - datetime.timedelta(minutes=30)

        mock_process_iter.return_value = []
        tracker.check_closed_games()
        mock_log_session.assert_called_once()

    def test_load_games(self):
        mock_connection = MagicMock()
        tracker = GameSessionTracker(mock_connection, games_file='games.json')

        with patch('builtins.open', unittest.mock.mock_open(read_data=json.dumps({
            "Cyberpunk 2077": "Cyberpunk2077.exe"
        }))):
            games = tracker.load_games()
            self.assertIn("Cyberpunk 2077", games)
            self.assertEqual(games["Cyberpunk 2077"], "Cyberpunk2077.exe")

if __name__ == '__main__':
    unittest.main()
