import unittest
import csv
import statistics
import random
from top_covering import top_cover
from pac_top_covering import pac_top_cover, precalculate_valuations_and_coalitions
from game_generator import check_core_stable
from votes_to_game import value_matrix_to_preferences, partition_edit_distance


class KnessetTestPacTopCovering(unittest.TestCase):

    def test_knesset(self):
        # run pac top cover
        votes, player_labels = knesset_votes_to_game()
        pi_pac = pac_top_cover(len(player_labels), votes)
        print_partition_stats(pi_pac)

        # run top cover
        value_matrix, coalition_matrix = precalculate_valuations_and_coalitions(votes)
        game = value_matrix_to_preferences(value_matrix, coalition_matrix)
        pi = top_cover(game)
        print_partition_stats(pi)

        edit_distance, paired_partitions = partition_edit_distance(pi, pi_pac)
        print(f'\nEdit distance between pac and original top covering output: {edit_distance}')
        print(paired_partitions)

        # check both partitions are stable
        self.assertTrue(check_core_stable(game, pi_pac))
        self.assertTrue(check_core_stable(game, pi))


    def test_knesset_sampling(self):
        random.seed(42)
        votes, player_labels = knesset_votes_to_game()
        sample_size = int(0.75 * len(votes))
        partitions = []

        with open('data/partitions_with_sampling_without_restriction_loop.csv', 'w') as f:
            csv_writer = csv.writer(f)
            for _ in range(100):
                pi = pac_top_cover(len(player_labels), votes, w=sample_size)
                print_partition_stats(pi)
                pi_labelled = index_to_label(player_labels, pi)
                row = [', '.join(coal) for coal in sorted(pi_labelled, key=len, reverse=True)]
                csv_writer.writerow(row)
                partitions.append(pi)

        distances = []
        for p1 in partitions:
            for p2 in partitions:
                if p1 == p2:
                    continue
                distances.append(partition_edit_distance(p1, p2)[0])
        print_partition_stability_stats(distances)


def knesset_votes_to_game():
    with open('data/votes_names.csv') as f:
        reader = csv.reader(f)
        player_labels = next(reader, None)
        player_labels = player_labels[1:]
        game = [[int(i) if i != '' else '' for i in row[1:]] for row in reader]
        return game, player_labels


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

if __name__ == '__main__':
    unittest.main()
