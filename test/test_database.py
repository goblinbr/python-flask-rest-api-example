import unittest

from app import database


class TestDatabase(unittest.TestCase):

    def test_last_id_should_be_2(self):
        self.assertEqual(2, database.lastId)

if __name__ == '__main__':
    unittest.main()