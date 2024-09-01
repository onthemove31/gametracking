import unittest
import logging
from game_tracker.utils import setup_logging

class TestUtilsModule(unittest.TestCase):

    def test_setup_logging(self):
        setup_logging()
        logger = logging.getLogger()
        self.assertEqual(logger.level, logging.INFO)

if __name__ == '__main__':
    unittest.main()
