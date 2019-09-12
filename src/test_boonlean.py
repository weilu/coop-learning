import unittest
from boonlean import votes_to_pref_tables


class TestBoonlean(unittest.TestCase):

    def test_votes_to_pref_tables(self):
        votes = [
            [1, 1, 2],
        ]
        likes, dislikes = votes_to_pref_tables(votes)

        self.assertEqual(len(likes), 3)
        self.assertEqual(likes[0], [frozenset([0, 1])])
        self.assertEqual(likes[1], [frozenset([0, 1])])
        self.assertEqual(likes[2], [frozenset([2])])

        self.assertEqual(len(dislikes), 3)
        self.assertEqual(dislikes[0], [frozenset([0, 2])])
        self.assertEqual(dislikes[1], [frozenset([1, 2])])
        self.assertEqual(dislikes[2], [frozenset([0, 1, 2])])

        votes = [
            [1, 1, 2],
            [2, 1, 2],
            [2, 2, 2],
        ]
        likes, dislikes = votes_to_pref_tables(votes)

        self.assertEqual(len(likes), 3)
        self.assertEqual(likes[0], [frozenset([0, 1]), frozenset([0, 2]), frozenset([0, 1, 2])])
        self.assertEqual(likes[1], [frozenset([0, 1]), frozenset([1]), frozenset([0, 1, 2])])
        self.assertEqual(likes[2], [frozenset([2]), frozenset([0, 2]), frozenset([0, 1, 2])])

        self.assertEqual(len(dislikes), 3)
        self.assertEqual(dislikes[0], [frozenset([0, 2]), frozenset([0, 1]), frozenset([0])])
        self.assertEqual(dislikes[1], [frozenset([1, 2]), frozenset([0, 1, 2]), frozenset([1])])
        self.assertEqual(dislikes[2], [frozenset([0, 1, 2]), frozenset([1, 2]), frozenset([2])])

        votes = [
            [1, 1, 2],
            [3, 1, 3],
            [3, 2, 3],
            [3, 1, 2],
        ]
        likes, dislikes = votes_to_pref_tables(votes)

        self.assertEqual(len(likes), 3)
        self.assertEqual(likes[0], [frozenset([0, 1])])
        self.assertEqual(likes[1], [frozenset([0, 1]), frozenset([1]), frozenset([1]), frozenset([1])])
        self.assertEqual(likes[2], [frozenset([2]), frozenset([2])])

        self.assertEqual(len(dislikes), 3)
        self.assertEqual(dislikes[0], [frozenset([0, 2])])
        self.assertEqual(dislikes[1], [frozenset([1, 2]), frozenset([1, 2])])
        self.assertEqual(dislikes[2], [frozenset([0, 1, 2]), frozenset([1, 2])])


if __name__ == '__main__':
    unittest.main()

