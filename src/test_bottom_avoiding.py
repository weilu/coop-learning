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

        # same game as above, reordered, different core produced
        # so core is not unique
        reordered_game = {}
        reordered_game[2] = game[2]
        reordered_game[3] = game[3]
        reordered_game[1] = game[1]

        pi = bottom_avoid(reordered_game)
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({2, 3}) in pi)
        self.assertTrue(frozenset({1}) in pi)

        # TODO: add more test cases


if __name__ == '__main__':
    unittest.main()
