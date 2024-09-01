import unittest
import sqlite3
import os
from game_tracker.database import store_session, cache_game_name, get_cached_game_name

class TestDatabaseModule(unittest.TestCase):

    def setUp(self):
        # Set up in-memory databases for testing
        self.session_conn = sqlite3.connect(':memory:')
        self.session_cursor = self.session_conn.cursor()
        self.session_cursor.execute('''CREATE TABLE sessions (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       exe_name TEXT NOT NULL,
                                       game_name TEXT NOT NULL,
                                       start_time TEXT NOT NULL,
                                       end_time TEXT NOT NULL,
                                       duration REAL)''')
        
        self.cache_conn = sqlite3.connect(':memory:')
        self.cache_cursor = self.cache_conn.cursor()
        self.cache_cursor.execute('''CREATE TABLE game_cache (
                                     exe_name TEXT PRIMARY KEY,
                                     game_name TEXT NOT NULL)''')

    def test_store_session(self):
        store_session('Cyberpunk2077.exe', 'Cyberpunk 2077', '2023-01-01 10:00:00', '2023-01-01 11:00:00', 60)
        self.session_cursor.execute("SELECT * FROM sessions WHERE exe_name=?", ('Cyberpunk2077.exe',))
        result = self.session_cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'Cyberpunk2077.exe')

    def test_cache_game_name(self):
        cache_game_name('Cyberpunk2077.exe', 'Cyberpunk 2077')
        self.cache_cursor.execute("SELECT * FROM game_cache WHERE exe_name=?", ('Cyberpunk2077.exe',))
        result = self.cache_cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'Cyberpunk 2077')

    def test_get_cached_game_name(self):
        cache_game_name('Cyberpunk2077.exe', 'Cyberpunk 2077')
        game_name = get_cached_game_name('Cyberpunk2077.exe')
        self.assertEqual(game_name, 'Cyberpunk 2077')

    def tearDown(self):
        # Close connections after each test
        self.session_conn.close()
        self.cache_conn.close()

if __name__ == '__main__':
    unittest.main()
