import unittest

from database import Database

class TestDatabase(unittest.TestCase):

    def test_smoke(self):
        database = Database()
        database.fetch_all_cars()

if __name__ == '__main__':
    unittest.main()