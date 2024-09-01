import unittest
from unittest.mock import patch, MagicMock
from game_tracker.game_tracker import track_game_sessions

class TestGameTrackerModule(unittest.TestCase):

    @patch('game_tracker.game_tracker.psutil.process_iter')
    @patch('game_tracker.game_tracker.get_game_name_from_igdb')
    @patch('game_tracker.game_tracker.store_session')
    def test_track_game_sessions(self, mock_store_session, mock_get_game_name, mock_process_iter):
        mock_process = MagicMock()
        mock_process.info = {'pid': 1234, 'name': 'Cyberpunk2077.exe'}
        mock_process_iter.return_value = [mock_process]
        mock_get_game_name.return_value = 'Cyberpunk 2077'

        # Simulate one iteration of the loop
        track_game_sessions()

        mock_get_game_name.assert_called_once_with('Cyberpunk2077.exe')
        mock_store_session.assert_not_called()  # Should not be called until game stops

if __name__ == '__main__':
    unittest.main()
