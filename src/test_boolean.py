import copy
import logging
import random
import unittest
from boolean import votes_to_pref_tables, simplify_pref_tables, find_core, find_pac_core
from knesset_test import print_partition_stats, calculate_partition_edit_distances_and_print_stats
from votes_to_game import read_votes_and_player_data


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


class TestBoolean(unittest.TestCase):

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
        self.assertEqual(likes[0], [frozenset([0, 1]), None, None, None])
        self.assertEqual(likes[1], [frozenset([0, 1]), frozenset([1]), frozenset([1]), frozenset([1])])
        self.assertEqual(likes[2], [frozenset([2]), None, None, frozenset([2])])

        self.assertEqual(len(dislikes), 3)
        self.assertEqual(dislikes[0], [frozenset([0, 2]), None, None, None])
        self.assertEqual(dislikes[1], [frozenset([1, 2]), None, None, frozenset([1, 2])])
        self.assertEqual(dislikes[2], [frozenset([0, 1, 2]), None, None, frozenset([1, 2])])


    def test_simplify_pref_tables(self):
        likes = {
            0: [frozenset({0, 1}), frozenset({0, 2}), frozenset({0, 1, 2})],
            1: [frozenset({0, 1}), frozenset({1}), frozenset({0, 1, 2})],
            2: [frozenset({2}), frozenset({0, 2}), frozenset({0, 1, 2})]
        }
        dislikes = {
            0: [frozenset({0, 2}), frozenset({0, 1}), frozenset({0})],
            1: [frozenset({1, 2}), frozenset({0, 1, 2}), frozenset({1})],
            2: [frozenset({0, 1, 2}), frozenset({1, 2}), frozenset({2})]
        }
        sl, sd = simplify_pref_tables(likes, dislikes)
        self.assertEqual(sl, {
            0: [frozenset({0, 1, 2})],
            1: [frozenset({0, 1})],
            2: [frozenset({0, 2})]
        })
        self.assertEqual(sd, {
            0: [frozenset({0, 1}), frozenset({0, 2}), frozenset({0})],
            1: [frozenset({0, 1, 2}), frozenset({1, 2}), frozenset({1})],
            2: [frozenset({0, 1, 2}), frozenset({1, 2}), frozenset({2})]
        })

        likes = {
            0: [frozenset({0, 1}), None, None, None],
            1: [frozenset({0, 1}), frozenset({1}), frozenset({1}), frozenset({1})],
            2: [frozenset({2}), None, None, frozenset({2})]
        }
        dislikes = {
            0: [frozenset({0, 2}), None, None, None],
            1: [frozenset({1, 2}), None, None, frozenset({1, 2})],
            2: [frozenset({0, 1, 2}), None, None, frozenset({1, 2})]
        }
        sl, sd = simplify_pref_tables(likes, dislikes)
        self.assertEqual(sl, {
            0: [frozenset({0, 1})],
            1: [frozenset({0, 1}), frozenset({1})],
            2: [frozenset({2})]
        })
        self.assertEqual(sd, {
            0: [frozenset({0, 2})],
            1: [frozenset({1, 2})],
            2: [frozenset({0, 1, 2}), frozenset({1, 2})]
        })


    def test_find_core(self):
        likes = {
            0: [frozenset({0, 1})],
            1: [frozenset({0, 1}), frozenset({1})],
            2: [frozenset({2})]
        }
        dislikes = {
            0: [frozenset({0, 2})],
            1: [frozenset({1, 2})],
            2: [frozenset({0, 1, 2}), frozenset({1, 2})]
        }
        pi = find_core(likes, dislikes)
        self.assertEqual(pi, {frozenset({0, 1}), frozenset({2})})

        likes = {
            0: [frozenset({0, 1, 2})],
            1: [frozenset({0, 1})],
            2: [frozenset({0, 2})]
        }
        dislikes = {
            0: [frozenset({0, 1}), frozenset({0, 2}), frozenset({0})],
            1: [frozenset({0, 1, 2}), frozenset({1})],
            2: [frozenset({0, 1, 2}), frozenset({2})]
        }
        pi = find_core(likes, dislikes)
        self.assertEqual(pi, {frozenset({0}), frozenset({1, 2})})

        likes = {
            0: [frozenset({0, 1, 2})],
            1: [frozenset({0, 1})],
            2: [frozenset({0, 2})]
        }
        dislikes = {
            0: [frozenset({0, 1}), frozenset({0, 2}), frozenset({0})],
            1: [frozenset({0, 1, 2}), frozenset({1, 2}), frozenset({1})],
            2: [frozenset({0, 1, 2}), frozenset({1, 2}), frozenset({2})]
        }
        pi = find_core(likes, dislikes)
        self.assertEqual(pi, {frozenset({0}), frozenset({1}), frozenset({2})})


    def test_pac_knesset(self):
        random.seed(42)
        original_votes, _ = read_votes_and_player_data()
        logging.info('done reading votes data')

        sample_size = int(0.75 * len(original_votes))
        partitions = []

        with open('data/partitions_pac_likes_dislikes_10_runs.txt', 'w') as f:
            for _ in range(10):
                votes = copy.deepcopy(original_votes)
                pi = find_pac_core(votes, sample_size)
                f.write(str(pi) + '\n')
                print(pi)
                print_partition_stats(pi)
                partitions.append(pi)

        calculate_partition_edit_distances_and_print_stats(partitions)


    def test_knesset(self):
        votes, _ = read_votes_and_player_data()
        logging.info('done reading votes data')
        likes, dislikes = votes_to_pref_tables(votes)
        logging.info('done constructing pref tables')
        likes, dislikes = simplify_pref_tables(likes, dislikes)
        logging.info('done simplifying pref tables')
        pi = find_core(likes, dislikes)
        print_partition_stats(pi)


if __name__ == '__main__':
    unittest.main()

