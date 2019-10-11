import copy
import logging
import random
import unittest
from boolean import votes_to_pref_table, find_core, find_pac_core
from knesset_test import print_partition_stats, calculate_partition_edit_distances_and_print_stats
from votes_to_game import read_votes_and_player_data


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


class TestBoolean(unittest.TestCase):

    def test_votes_to_pref_table(self):
        votes = [
            [1, 1, 2],
        ]
        prefs = votes_to_pref_table(votes)

        self.assertEqual(len(prefs), 3)
        self.assertEqual(prefs[0], [frozenset([0, 1])])
        self.assertEqual(prefs[1], [frozenset([0, 1])])
        self.assertEqual(prefs[2], [frozenset([2])])

        votes = [
            [1, 1, 2],
            [2, 1, 2],
            [2, 2, 2],
        ]
        prefs = votes_to_pref_table(votes)

        self.assertEqual(len(prefs), 3)
        self.assertEqual(prefs[0], [frozenset([0, 1]), frozenset([0, 2]), frozenset([0, 1, 2])])
        self.assertEqual(prefs[1], [frozenset([0, 1]), frozenset([1]), frozenset([0, 1, 2])])
        self.assertEqual(prefs[2], [frozenset([2]), frozenset([0, 2]), frozenset([0, 1, 2])])

        votes = [
            [1, 1, 2],
            [3, 1, 3],
            [3, 2, 3],
            [3, 1, 2],
        ]
        prefs = votes_to_pref_table(votes)

        self.assertEqual(len(prefs), 3)
        self.assertEqual(prefs[0], [frozenset([0, 1]), None, None, None])
        self.assertEqual(prefs[1], [frozenset([0, 1]), frozenset([1]), frozenset([1]), frozenset([1])])
        self.assertEqual(prefs[2], [frozenset([2]), None, None, frozenset([2])])


    def test_find_core(self):
        prefs = {
            0: [frozenset({0, 1})],
            1: [frozenset({0, 1}), frozenset({1})],
            2: [frozenset({2})]
        }
        pi = find_core(prefs)
        self.assertEqual(pi, {frozenset({0, 1}), frozenset({2})})

        prefs = {
            0: [frozenset([0, 1]), frozenset([0, 2]), frozenset([0, 1, 2])],
            1: [frozenset([0, 1]), frozenset([1]), frozenset([0, 1, 2])],
            2: [frozenset([2]), frozenset([0, 2]), frozenset([0, 1, 2])]
        }
        pi = find_core(prefs)
        self.assertEqual(pi, {frozenset({0, 1, 2})})

        prefs = {
            0: [frozenset([0, 1]), None, None, None],
            1: [frozenset([0, 1]), frozenset([1]), frozenset([1]), frozenset([1])],
            2: [frozenset([2]), None, None, frozenset([2])]
        }
        pi = find_core(prefs)
        self.assertEqual(pi, {frozenset({0, 1}), frozenset({2})})


    def test_find_pac_core(self):
        votes = [
            [1, 1, 2],
            [3, 1, 3],
            [3, 2, 3],
            [3, 1, 2],
        ]
        prefs = votes_to_pref_table(votes)
        pi_core = find_core(prefs)
        pi_pac_core = find_pac_core(votes, len(votes), sample_method=random.sample)
        self.assertEqual(pi_core, pi_pac_core)

        # test on knesset data
        votes, _ = read_votes_and_player_data()
        logging.info('done reading votes data')
        prefs = votes_to_pref_table(votes)
        logging.info('done constructing pref tables')
        pi_core = find_core(prefs)
        logging.info('done finding core')
        pi_pac_core = find_pac_core(votes, len(votes), sample_method=random.sample)
        logging.info('done finding pac core')

        self.assertEqual(pi_core, pi_pac_core)

        print(pi_pac_core)
        print_partition_stats(pi_pac_core)


    def test_pac_knesset(self):
        random.seed(42)
        original_votes, _ = read_votes_and_player_data()
        logging.info('done reading votes data')

        sample_size = int(0.75 * len(original_votes))
        partitions = []

        with open('data/partitions_pac_boolean_50_runs.txt', 'w') as f:
            for round in range(50):
                votes = copy.deepcopy(original_votes)
                pi = find_pac_core(votes, sample_size)
                f.write(str(pi) + '\n')
                print(pi)
                print_partition_stats(pi)
                partitions.append(pi)
                logging.info(f'done round {round + 1}')

        calculate_partition_edit_distances_and_print_stats(partitions)


    def test_knesset(self):
        votes, _ = read_votes_and_player_data()
        logging.info('done reading votes data')
        prefs = votes_to_pref_table(votes)
        logging.info('done constructing pref tables')
        pi = find_core(prefs)
        print(pi)
        print_partition_stats(pi)

        with open('data/partitions_boolean_1_runs.txt', 'w') as f:
            f.write(str(pi))


if __name__ == '__main__':
    unittest.main()

