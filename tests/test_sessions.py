import unittest
from unittest.mock import MagicMock
from database.sessions import create_sessions_table, log_session
import datetime  # Import datetime to create datetime objects

class TestDatabaseSessions(unittest.TestCase):

    def test_create_sessions_table(self):
        mock_cursor = MagicMock()
        create_sessions_table(mock_cursor)
        mock_cursor.execute.assert_called_once()

    def test_log_session(self):
        mock_cursor = MagicMock()

        # Use datetime objects instead of strings
        start_time = datetime.datetime.strptime("2024-08-27 12:00:00", '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime("2024-08-27 12:30:00", '%Y-%m-%d %H:%M:%S')

        log_session(mock_cursor, "Cyberpunk2077.exe", "Cyberpunk 2077",
                    start_time, end_time, 30)
        mock_cursor.execute.assert_called_once()
        mock_cursor.connection.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
