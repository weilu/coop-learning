import unittest
import random
from knesset_test import print_partition_stats
from friends import find_friends
from enemies import to_avoid_sets, bottom_avoid, pac_bottom_avoid
from votes_to_game import read_votes_and_player_data


class TestEnemies(unittest.TestCase):

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


    def test_knesset(self):
        votes, player_labels = read_votes_and_player_data()
        friend_matrix = find_friends(votes)
        pi = bottom_avoid(friend_matrix)
        print(pi)
        print_partition_stats(pi)
        # TODO: verify core stable


    def test_pac_bottom_avoid(self):
        votes = [
            [1, 1, 2],
            [1, 2, 2],
            [2, 2, 2],
        ]

        friend_matrix = find_friends(votes)
        pi = bottom_avoid(friend_matrix)

        pi_pac = pac_bottom_avoid(votes, len(votes), sample_method=random.sample)
        self.assertEqual(pi, pi_pac)

        # use knesset data
        votes, player_labels = read_votes_and_player_data()
        friend_matrix = find_friends(votes)
        pi = bottom_avoid(friend_matrix)
        pi_pac = pac_bottom_avoid(votes, len(votes), sample_method=random.sample)
        self.assertEqual(pi, pi_pac)

if __name__ == '__main__':
    unittest.main()
