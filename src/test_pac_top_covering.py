import unittest
import csv
import statistics
import random
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

    def test_knesset(self):
        random.seed(42)
        with open('data/votes.csv') as f:
            reader = csv.reader(f)
            player_labels = next(reader, None)
            player_labels = player_labels[1:]
            votes = [[int(i) for i in row[1:]] for row in reader]
            pi = pac_top_cover(len(player_labels), votes)
            print(pi)
            print_partition_stats(pi)
            # print(index_to_label(player_labels, pi))


def index_to_label(player_labels, pi):
    labelled_pi = set()
    for s in pi:
        labelled_pi.add(frozenset([player_labels[i] for i in s]))
    return labelled_pi


def print_partition_stats(pi):
    num_coalitions = len(pi)
    coalition_sizes = list(map(len, pi))
    max_coalition_size = max(coalition_sizes)
    min_coalition_size = min(coalition_sizes)
    mean_coalition_size = statistics.mean(coalition_sizes)
    median_coalition_size = statistics.median(coalition_sizes)
    print(f'Number of coalitions: {num_coalitions},\n'
          f'max: {max_coalition_size},\n'
          f'min: {min_coalition_size},\n'
          f'mean: {mean_coalition_size}, \n'
          f'median: {median_coalition_size}')


if __name__ == '__main__':
    unittest.main()
