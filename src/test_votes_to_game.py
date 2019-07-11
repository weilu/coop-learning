import unittest
from votes_to_game import majority, value_function, get_coalition


class TestVotesToGame(unittest.TestCase):

    def test_majority(self):
        x = [1, 1, 1]
        self.assertEqual(majority(x), 1)

        x = [2]
        self.assertEqual(majority(x), 2)

        x = [0, 0, 1, 1, 2, 3, 4]
        self.assertEqual(majority(x), 1)

        x = [0, 0, 0]
        self.assertEqual(majority(x), 2)

        x = [1, 2]
        self.assertEqual(majority(x), 2)

    def test_value_function(self):
        x = [1, 1, 1]
        self.assertEqual(value_function(0, x, 1), 1 + 1/3)

        x = [0, 1, 1]
        self.assertEqual(value_function(0, x, 1), 0)

        x = [1, 1, 0]
        self.assertEqual(value_function(0, x, 1), 1.5)

    def test_get_coalition(self):
        x = [1, 1, 1]
        self.assertEqual(get_coalition(0, x, 1), {0, 1, 2})

        x = [0, 1, 1]
        self.assertEqual(get_coalition(0, x, 1), {0})

        x = [1, 1, 0]
        self.assertEqual(get_coalition(0, x, 1), {0, 1})


if __name__ == '__main__':
    unittest.main()
