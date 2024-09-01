import unittest
import pandas as pd
from modules.recommendations import recommend_games_based_on_played

class TestRecommendations(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        data = {
            'game_name': ['Game A', 'Game B'],
        }
        self.df = pd.DataFrame(data)

    def test_recommend_games_based_on_played(self):
        # Assuming you have a mock or live response from IGDB API for testing
        recommendations = recommend_games_based_on_played(self.df, None)
        self.assertIsInstance(recommendations, list)

if __name__ == '__main__':
    unittest.main()
