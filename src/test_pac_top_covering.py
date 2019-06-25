import unittest
import csv
from pac_top_covering import pac_top_cover


class TestPacTopCovering(unittest.TestCase):

    def test_simple(self):
        pi = pac_top_cover(7, [[1, 1, 1, 2, 2, 2, 1],
                               [1, 1, 1, 2, 2, 2, 2], ])
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({0, 1, 2, 6}) in pi)
        self.assertTrue(frozenset({3, 4, 5}) in pi)

    def test_knesset(self):
        with open('data/votes.csv') as f:
            reader = csv.reader(f)
            player_labels = next(reader, None)
            player_labels = player_labels[1:]
            votes = [[int(i) for i in row[1:]] for row in reader]
            pi = pac_top_cover(len(player_labels), votes)
            print(pi)
            print(index_to_label(player_labels, pi))


def index_to_label(player_labels, pi):
    labelled_pi = set()
    for s in pi:
        labelled_pi.add(frozenset([player_labels[i] for i in s]))
    return labelled_pi


if __name__ == '__main__':
    unittest.main()
