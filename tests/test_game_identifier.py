import unittest
from unittest.mock import patch
from game_tracker.game_identifier import get_game_name_from_igdb
from game_tracker.database import cache_game_name

class TestGameIdentifierModule(unittest.TestCase):

    @patch('game_tracker.game_identifier.requests.post')
    def test_get_game_name_from_igdb_cache_hit(self, mock_post):
        cache_game_name('Cyberpunk2077.exe', 'Cyberpunk 2077')
        game_name = get_game_name_from_igdb('Cyberpunk2077.exe')
        self.assertEqual(game_name, 'Cyberpunk 2077')
        mock_post.assert_not_called()  # API should not be called if cache hit

    @patch('game_tracker.game_identifier.requests.post')
    def test_get_game_name_from_igdb_cache_miss(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = [{'name': 'Cyberpunk 2077'}]
        
        game_name = get_game_name_from_igdb('Cyberpunk2077.exe')
        self.assertEqual(game_name, 'Cyberpunk 2077')
        mock_post.assert_called_once()  # API should be called if cache miss

    @patch('game_tracker.game_identifier.requests.post')
    def test_get_game_name_from_igdb_failure(self, mock_post):
        mock_post.return_value.status_code = 404
        game_name = get_game_name_from_igdb('UnknownGame.exe')
        self.assertIsNone(game_name)

if __name__ == '__main__':
    unittest.main()
