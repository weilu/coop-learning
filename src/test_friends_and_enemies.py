import unittest
from knesset_test import read_votes_and_player_data, print_partition_stats
from friends_and_enemies import stable_friends, find_friends, top_cover, to_avoid_sets, bottom_avoid


class TestFriendsAndEnemies(unittest.TestCase):

    def test_knesset(self):
        votes, player_labels = read_votes_and_player_data()
        friend_matrix = find_friends(votes)
        pi = stable_friends(friend_matrix)
        print(pi)
        print_partition_stats(pi)

        pi_tc = top_cover(friend_matrix)
        self.assertEqual(pi, pi_tc)
        # TODO: verify core stable

        pi_ba = bottom_avoid(friend_matrix)
        print(pi_ba)
        print_partition_stats(pi_ba)
        # TODO: verify core stable

    def test_find_friends(self):
        friend_matrix = find_friends([[1, 1, 2]])
        self.assertEqual(len(friend_matrix), 3)
        self.assertTrue(1 in friend_matrix[0])
        self.assertTrue(0 in friend_matrix[1])
        self.assertFalse(friend_matrix[2])

        friend_matrix = find_friends([[3, 1, 3]])
        self.assertFalse(friend_matrix[0])
        self.assertFalse(friend_matrix[1])
        self.assertFalse(friend_matrix[2])

        friend_matrix = find_friends([
            [1, 1, 2],
            [2, 1, 2],
            ])
        self.assertFalse(friend_matrix[0])
        self.assertFalse(friend_matrix[1])
        self.assertFalse(friend_matrix[2])

        friend_matrix = find_friends([
            [1, 1, 2],
            [2, 1, 2],
            [2, 2, 2],
            ])
        self.assertTrue(1 in friend_matrix[0])
        self.assertTrue(2 in friend_matrix[0])
        self.assertTrue(0 in friend_matrix[1])
        self.assertTrue(0 in friend_matrix[2])


    def test_stable_friends(self):
        friend_matrix = [{1, 2}, {0}, {0}]
        pi = stable_friends(friend_matrix)
        self.assertEqual(len(pi), 1)
        self.assertTrue(frozenset({0, 1, 2}) in pi)
        pi_tc = top_cover(friend_matrix)
        self.assertEqual(pi, pi_tc)

        friend_matrix = [{1}, {0}, set()]
        pi = stable_friends(friend_matrix)
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({0, 1}) in pi)
        self.assertTrue(frozenset({2}) in pi)
        pi_tc = top_cover(friend_matrix)
        self.assertEqual(pi, pi_tc)

        friend_matrix = [{1}, {}, {0, 1}]
        pi = stable_friends(friend_matrix)
        self.assertEqual(len(pi), 3)
        self.assertTrue(frozenset({0}) in pi)
        self.assertTrue(frozenset({1}) in pi)
        self.assertTrue(frozenset({2}) in pi)
        pi_tc = top_cover(friend_matrix)
        self.assertEqual(pi, pi_tc)

        friend_matrix = find_friends([
            [1, 1, 2],
            [3, 1, 3],
            [3, 2, 3],
        ])
        self.assertTrue(1 in friend_matrix[0])
        self.assertTrue(0 in friend_matrix[1])
        self.assertFalse(friend_matrix[2])


    def test_to_avoid_sets(self):
        friend_matrix = [{1, 2}, {0}, {0}]
        avoid_sets = to_avoid_sets(friend_matrix)
        self.assertEqual(len(avoid_sets), 3)
        self.assertEqual(avoid_sets[0], {0})
        self.assertEqual(avoid_sets[1], {1, 2})
        self.assertEqual(avoid_sets[2], {1, 2})

        friend_matrix = [None, {0}, {0}]
        avoid_sets = to_avoid_sets(friend_matrix)
        self.assertEqual(len(avoid_sets), 2)
        self.assertEqual(avoid_sets[1], {1, 2})
        self.assertEqual(avoid_sets[2], {1, 2})

        friend_matrix = [None, {2}, {0}]
        avoid_sets = to_avoid_sets(friend_matrix)
        self.assertEqual(len(avoid_sets), 2)
        self.assertEqual(avoid_sets[1], {1})
        self.assertEqual(avoid_sets[2], {1, 2})

        friend_matrix = [None, None, {0}]
        avoid_sets = to_avoid_sets(friend_matrix)
        self.assertEqual(len(avoid_sets), 1)
        self.assertEqual(avoid_sets[2], {2})

        friend_matrix = [None, None, set()]
        avoid_sets = to_avoid_sets(friend_matrix)
        self.assertEqual(len(avoid_sets), 1)
        self.assertEqual(avoid_sets[2], {2})


    def test_bottom_avoid(self):
        friend_matrix = [{1}, {0, 2}, {1}]
        pi = bottom_avoid(friend_matrix)
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({0, 1}) in pi)
        self.assertTrue(frozenset({2}) in pi)

        #TODO: add more test cases


if __name__ == '__main__':
    unittest.main()
