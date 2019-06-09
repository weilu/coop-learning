import unittest
from top_covering import top_cover


class TestTopCovering(unittest.TestCase):

    # Example 15.5, Handbook of Computational Social Choice, p365
    # https://doi.org/10.1017/CBO9781107446984.016
    def test_simple(self):
        sample = {
            1: [{1, 2}, {1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 3}, {1, 3, 4}, {1, 4}, {1}],
            2: [{2, 3}, {2, 3, 4}, {1, 2, 3}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 2}, {2}],
            3: [{1, 3}, {1, 2, 3}, {1, 3, 4}, {1, 2, 3, 4}, {2, 3}, {2, 3, 4}, {3, 4}, {3}],
            4: [{3, 4}, {2, 3, 4}, {1, 3, 4}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 4}, {4}]
        }
        pi = top_cover(sample)
        self.assertEqual(len(pi), 2)
        self.assertEqual(pi[0], frozenset({1, 2, 3}))
        self.assertEqual(pi[1], frozenset({4}))

    def test_simple_modified(self):
        sample = {
            1: [{1, 2}, {1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 3}, {1, 3, 4}, {1, 4}, {1}],
            2: [{2, 3}, {2, 3, 4}, {1, 2, 3}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 2}, {2}],
            3: [{1, 3}, {1, 2, 3}, {1, 3, 4}, {1, 2, 3, 4}, {2, 3}, {2, 3, 4}, {3, 4}, {3}],
            4: [{3, 4}, {4, 5}, {4}],
            5: [{4, 5}, {5}]
        }
        pi = top_cover(sample)
        self.assertEqual(len(pi), 2)
        self.assertEqual(pi[0], frozenset({1, 2, 3}))
        self.assertEqual(pi[1], frozenset({4, 5}))

    def test_all_in_one(self):
        sample = {
            1: [{1, 2}],
            2: [{2, 3, 6}],
            3: [{1, 3}],
            4: [{3, 4, 5}],
            5: [{4, 5, 6}],
            6: [{4, 6}],
        }
        pi = top_cover(sample)
        self.assertEqual(len(pi), 1)
        self.assertEqual(pi[0], frozenset({1, 2, 3, 4, 5, 6}))

    def test_multiple_iteration(self):
        sample = {
            1: [{1, 2}],
            2: [{2, 3}, {2, 6}],
            3: [{1, 3}],
            4: [{3, 4}, {4, 5}],
            5: [{4, 5}, {5, 6}],
            6: [{4, 6}],
        }
        pi = top_cover(sample)
        self.assertEqual(len(pi), 3)
        self.assertEqual(pi[0], frozenset({1, 2, 3}))
        self.assertEqual(pi[1], frozenset({4, 5}))
        self.assertEqual(pi[2], frozenset({6}))


if __name__ == '__main__':
    unittest.main()
