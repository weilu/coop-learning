import unittest
from bottom_avoiding import bottom_avoid

class TestBottomAvoiding(unittest.TestCase):

    def test_bottom_avoid(self):
        game = {
            1: [{1, 2}, {1}, {1, 2, 3}, {1, 3}],
            2: [{1, 2, 3}, {1, 2}, {2, 3}, {2}],
            3: [{2, 3}, {3}, {1, 2, 3}, {1, 3}],
        }
        pi = bottom_avoid(game)
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({1, 2}) in pi)
        self.assertTrue(frozenset({3}) in pi)


if __name__ == '__main__':
    unittest.main()
