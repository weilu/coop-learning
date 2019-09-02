import csv
import unittest
from votes_to_game import majority, value_function, get_coalition, value_matrix_to_preferences, partition_edit_distance, filter_infrequent_voters, read_votes_and_player_data


class TestVotesToGame(unittest.TestCase):

    def test_majority(self):
        x = [1, 1, 1]
        self.assertEqual(majority(x), 1)

        x = [2]
        self.assertEqual(majority(x), 2)

        x = [0, 0, 1, 1, 2, 3, 4]
        self.assertEqual(majority(x), 1)

        x = [0, 0, 0]
        self.assertEqual(majority(x), 2)

        x = [1, 2]
        self.assertEqual(majority(x), 2)

    def test_value_function(self):
        x = [1, 1, 1]
        self.assertEqual(value_function(0, x, 1), 1 + 1/3)

        x = [0, 1, 1]
        self.assertEqual(value_function(0, x, 1), 0)

        x = [1, 1, 0]
        self.assertEqual(value_function(0, x, 1), 1.5)

    def test_get_coalition(self):
        x = [1, 1, 1]
        self.assertEqual(get_coalition(0, x, 1), {0, 1, 2})

        x = [0, 1, 1]
        self.assertEqual(get_coalition(0, x, 1), {0})

        x = [1, 1, 0]
        self.assertEqual(get_coalition(0, x, 1), {0, 1})

    def test_value_matrix_to_preferences(self):
        # generated from S = [[1, 1, 2, 2], [1, 1, 1, 1], ]
        value_matrix = [[0, 0, 1.5, 1.5],
                        [1.25, 1.25, 1.25, 1.25]]
        coalition_matrix = [[{0}, {1}, {2, 3}, {2, 3}],
                            [{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}]]
        game = value_matrix_to_preferences(value_matrix, coalition_matrix)
        self.assertEqual(game[0], [{0, 1, 2, 3}])
        self.assertEqual(game[1], [{0, 1, 2, 3}])
        self.assertEqual(game[2], [{2, 3}, {0, 1, 2, 3}])
        self.assertEqual(game[3], [{2, 3}, {0, 1, 2, 3}])

        # check that duplicates and 0 values are dropped
        value_matrix.append(value_matrix[0])
        coalition_matrix.append(coalition_matrix[0])
        game = value_matrix_to_preferences(value_matrix, coalition_matrix)
        self.assertEqual(game[0], [{0, 1, 2, 3}])
        self.assertEqual(game[3], [{2, 3}, {0, 1, 2, 3}])

    def test_partition_edit_distance(self):
        dist, _ = partition_edit_distance(
                {frozenset({1, 2}), frozenset({3})},
                {frozenset({1, 2}), frozenset({3})})
        self.assertEqual(dist, 0)

        dist, pairs = partition_edit_distance(
                {frozenset({1, 2}), frozenset({3})},
                {frozenset({1, 2, 3})})
        self.assertEqual(dist, 2)
        self.assertEqual(pairs[1], (frozenset({1, 2}), frozenset({1, 2, 3})))
        self.assertEqual(pairs[0], (frozenset({3}), frozenset({})))

        dist, pairs = partition_edit_distance(
                {frozenset({1, 2}), frozenset({3, 4}), frozenset({5})},
                {frozenset({1}), frozenset({2}), frozenset({3, 4, 5})})
        self.assertEqual(dist, 4)

        dist, pairs = partition_edit_distance(
                {frozenset({1, 2}), frozenset({3, 4}), frozenset({5}), frozenset({6})},
                {frozenset({1}), frozenset({2}), frozenset({3, 4, 5, 6})})
        self.assertEqual(dist, 6)

        dist, pairs = partition_edit_distance(
                {frozenset({1, 2, 3}), frozenset({4})},
                {frozenset({1, 2}), frozenset({3, 5, 6, 7, 8})})
        self.assertEqual(dist, 7)

        dist, pairs = partition_edit_distance(
                {frozenset({1, 2, 3})},
                {frozenset({})})
        self.assertEqual(dist, 3)


    def test_read_votes_and_player_data(self):
        votes, player_labels = read_votes_and_player_data()
        self.assertEqual(len(votes), 7489)
        for row in votes:
            self.assertEqual(len(row), 147)


    def test_filter_infrequent_voters(self):
        votes, player_labels = read_votes_and_player_data()
        new_votes, new_player_labels = filter_infrequent_voters(0)
        self.assertEqual(votes, new_votes)
        self.assertEqual(player_labels, new_player_labels)

        new_votes, new_player_labels = filter_infrequent_voters(1000)
        self.assertEqual(len(new_player_labels), 130)
        for row in new_votes:
            self.assertEqual(len(row), 130)

        with open('data/votes_names_cleaned_filtered.csv', 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['vote_id'] + new_player_labels)
            for i, row in enumerate(new_votes):
                csv_writer.writerow([i] + row)

if __name__ == '__main__':
    unittest.main()
