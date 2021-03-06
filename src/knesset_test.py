import unittest
import csv
import statistics
import random
from top_covering import top_cover
from pac_top_covering import pac_top_cover
from game_generator import check_core_stable, search_stable_partition, check_top_responsive
from votes_to_game import value_matrix_to_preferences, partition_edit_distance, precalculate_valuations_and_coalitions, read_votes_and_player_data


class KnessetTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.votes, cls.player_labels = read_votes_and_player_data()
        cls.value_matrix, cls.coalition_matrix = precalculate_valuations_and_coalitions(cls.votes)
        cls.game = value_matrix_to_preferences(cls.value_matrix, cls.coalition_matrix)


    def test_top_responsive(self):
        is_tr, violations = check_top_responsive(self.game, return_violations=True)
        print(f'Game generated from Knesset data is top responsive: {is_tr}')
        print(violations)


    def test_original_and_pac_top_covering(self):
        pi = top_cover(self.game)
        pi_pac = pac_top_cover(len(self.player_labels), self.votes)

        self.assertEqual(pi, pi_pac)

        with open('data/partitions_value_function_1_runs.txt', 'w') as f:
            f.write(str(pi))

        # check partition is stable
        self.assertTrue(check_core_stable(self.game, pi))

        print_partition_stats(pi)
        print(pi)
        pi_labelled = index_to_label(self.player_labels, pi)
        print(pi_labelled)


    def test_pac_with_sampling(self):
        random.seed(42)
        sample_size = int(0.75 * len(self.votes))
        partitions = []

        with open('data/partitions_pac_value_function_50_runs.txt', 'w') as f:
            for _ in range(50):
                pi = pac_top_cover(len(self.player_labels), self.votes, w=sample_size)
                print(pi)
                f.write(str(pi) + '\n')
                print_partition_stats(pi)
                # print(f'core stable: {check_core_stable(self.game, pi)}')
                partitions.append(pi)

        calculate_partition_edit_distances_and_print_stats(partitions)


    def test_search_and_split(self):
        max_len = 0
        for row in self.coalition_matrix:
            for el in row:
                if len(el) > max_len:
                    max_len = len(el)
        pi = search_stable_partition(self.game)
        print_partition_stats(pi)
        print(pi)


    def test_count_missing_votes(self):
        with open('data/votes_names.csv') as f:
            reader = csv.reader(f)
            next(reader, None)
            total_missing = 0
            total = 0
            for row in reader:
                missing = sum(1 if vote == '' else 0 for vote in row[1:])
                total_missing += missing
                total += sum(1 for vote in row[1:])
        print(f'missing vote value: {total_missing}, total number of votes: {total}, missing percentage: {round(total_missing/total * 100, 2)}%')


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
          f'coalition sizes:'
          f'    max: {max_coalition_size},\n'
          f'    min: {min_coalition_size},\n'
          f'    mean: {mean_coalition_size}, \n'
          f'    median: {median_coalition_size}')

def print_partition_stability_stats(edit_distances):
    max_dist = max(edit_distances)
    min_dist = min(edit_distances)
    mean_dist = statistics.mean(edit_distances)
    median_dist = statistics.median(edit_distances)
    print(f'Partition edit distances:\n'
          f'     max: {max_dist},\n'
          f'     min: {min_dist},\n'
          f'     mean: {mean_dist}, \n'
          f'     median: {median_dist}')

def calculate_partition_edit_distances_and_print_stats(partitions):
    distances = []
    for i in range(len(partitions) - 1):
        p1 = partitions[i]
        for j in range(i+1, len(partitions)):
            p2 = partitions[j]
            distances.append(partition_edit_distance(p1, p2)[0])
    print_partition_stability_stats(distances)

if __name__ == '__main__':
    unittest.main()
