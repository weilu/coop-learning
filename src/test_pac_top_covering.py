import unittest
from pac_top_covering import pac_top_cover


class TestPacTopCovering(unittest.TestCase):

    def test_simple(self):
        pi = pac_top_cover(7, [[1, 1, 1, 2, 2, 2, 1],
                               [1, 1, 1, 2, 2, 2, 2], ])
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({0, 1, 2, 6}) in pi)
        self.assertTrue(frozenset({3, 4, 5}) in pi)


    def test_simpler(self):
        pi = pac_top_cover(4, [[1, 1, 2, 2],
                               [1, 1, 1, 1], ])
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({0, 1}) in pi)
        self.assertTrue(frozenset({2, 3}) in pi)


if __name__ == '__main__':
    unittest.main()
