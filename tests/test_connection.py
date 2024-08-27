import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from database.connection import create_db_connection, close_db_connection

class TestDatabaseConnection(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_create_db_connection(self, mock_connect):
        mock_connect.return_value = MagicMock()
        conn = create_db_connection('test.db')
        mock_connect.assert_called_with('test.db')
        self.assertIsNotNone(conn)

    def test_close_db_connection(self):
        mock_connection = MagicMock()
        close_db_connection(mock_connection)
        mock_connection.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
