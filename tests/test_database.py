import unittest
import pandas as pd
from modules.analytics import get_detailed_session_analytics, analyze_gaming_habits

class TestAnalytics(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        data = {
            'game_name': ['Game A', 'Game B', 'Game C'],
            'start_time': pd.to_datetime(['2024-08-28 14:00:00', '2024-08-29 15:00:00', '2024-08-30 16:00:00']),
            'end_time': pd.to_datetime(['2024-08-28 15:00:00', '2024-08-29 16:00:00', '2024-08-30 17:00:00']),
            'duration': [60, 60, 60]
        }
        self.df = pd.DataFrame(data)

    def test_detailed_session_analytics(self):
        analytics = get_detailed_session_analytics(self.df)
        self.assertIn('session_distribution', analytics)
        self.assertIn('weekly_trends', analytics)
        self.assertIn('monthly_trends', analytics)

    def test_analyze_gaming_habits(self):
        late_night_percentage = analyze_gaming_habits(self.df)
        self.assertIsInstance(late_night_percentage, float)

if __name__ == '__main__':
    unittest.main()
