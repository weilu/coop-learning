import copy
import logging
import random
import unittest
from knesset_test import print_partition_stats, calculate_partition_edit_distances_and_print_stats
from votes_to_game import read_votes_and_player_data
from simple_likes import find_pac_core

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def find_biggest_coalition(votes):
    max_coalition = {}
    for row in votes:
        for_group = []
        against_group = []
        for i, vote in enumerate(row):
            if vote == 1:
                for_group.append(i)
            elif vote == 2:
                against_group.append(i)
        if len(for_group) > len(against_group):
            bigger_group = for_group
        else:
            bigger_group = against_group
        if len(bigger_group) > len(max_coalition):
            max_coalition = frozenset(bigger_group)
    return max_coalition


class TestSimpleLikes(unittest.TestCase):

    def test_pac_core(self):
        original_votes, _ = read_votes_and_player_data()
        votes = copy.deepcopy(original_votes)
        sample_size = len(votes)
        pi_pac = find_pac_core(votes, sample_size, random.sample)

        # effectively always finding & removing the biggest coalition
        votes = copy.deepcopy(original_votes)
        players = set(range(len(votes[0])))
        pi = set()
        while players:
            coalition = find_biggest_coalition(votes)
            pi.add(coalition)
            players = players - coalition

            for i, row in enumerate(votes):
                for j, vote in enumerate(row):
                    if j in coalition and vote in (1, 2):
                        row[j] = None

        self.assertEqual(pi_pac, pi)
        print(pi)
        print_partition_stats(pi)


    def test_pac_knesset(self):
        random.seed(42)
        original_votes, _ = read_votes_and_player_data()
        logging.info('done reading votes data')

        sample_size = int(0.75 * len(original_votes))
        partitions = []

        with open('data/partitions_pac_likes_10_runs.txt', 'w') as f:
            for _ in range(10):
                votes = copy.deepcopy(original_votes)
                pi = find_pac_core(votes, sample_size)
                f.write(str(pi) + '\n')
                print(pi)
                print_partition_stats(pi)
                partitions.append(pi)

        calculate_partition_edit_distances_and_print_stats(partitions)


if __name__ == '__main__':
    unittest.main()
