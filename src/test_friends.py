import copy
import random
import unittest
from knesset_test import print_partition_stats, calculate_partition_edit_distances_and_print_stats
from friends import stable_friends, find_friends, top_cover, pac_top_cover, precalculate_coalitions, precalculate_frenemy_per_player_per_bill
from top_covering import largest_scc_from_pref
from votes_to_game import partition_edit_distance, read_votes_and_player_data


class TestFriends(unittest.TestCase):

    def test_pac_top_cover(self):
        votes = [
            [1, 1, 2],
        ]
        diff_matrix = precalculate_frenemy_per_player_per_bill(votes, False)
        pi = pac_top_cover(votes, diff_matrix, sample_method=random.sample)
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({0, 1}) in pi)
        self.assertTrue(frozenset({2}) in pi)

        votes = [
            [1, 1, 2],
            [2, 1, 2],
            [2, 2, 2],
        ]
        diff_matrix = precalculate_frenemy_per_player_per_bill(votes, False)
        pi = pac_top_cover(votes, diff_matrix, sample_method=random.sample)
        self.assertEqual(len(pi), 1)
        self.assertTrue(frozenset({0, 1, 2}) in pi)

        votes = [
            [1, 1, 2],
            [3, 1, 3],
            [3, 2, 3],
        ]
        diff_matrix = precalculate_frenemy_per_player_per_bill(votes, False)
        pi = pac_top_cover(votes, diff_matrix, sample_method=random.sample)
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({0, 1}) in pi)
        self.assertTrue(frozenset({2}) in pi)


    def test_pac_knesset(self):
        random.seed(42)
        original_votes, _ = read_votes_and_player_data()
        sample_size = int(0.75 * len(original_votes))

        diff_matrix = precalculate_frenemy_per_player_per_bill(votes, False)
        with open('data/partitions_pac_friends_50_runs.txt', 'w') as f:
            for r in range(50):
                votes = copy.deepcopy(original_votes)
                pi = pac_top_cover(votes, diff_matrix, sample_size)
                print(pi)
                print_partition_stats(pi)
                print(f'done round {r + 1}')

        random.seed(42)
        diff_matrix = precalculate_frenemy_per_player_per_bill(votes, True)
        with open('data/partitions_pac_friends_selective_50_runs.txt', 'w') as f:
            for r in range(50):
                votes = copy.deepcopy(original_votes)
                pi = pac_top_cover(votes, diff_matrix, sample_size)
                print(pi)
                print_partition_stats(pi)
                print(f'done round {r + 1}')


    def test_knesset(self):
        votes, player_labels = read_votes_and_player_data()

        friend_matrix = find_friends(votes, selective_friends=False)
        with open('data/partitions_friends_1_runs.txt', 'w') as f:
            pi = stable_friends(friend_matrix)
            f.write(str(pi) + '\n')
            print(pi)
            print_partition_stats(pi)

            pi_tc = top_cover(friend_matrix)
            self.assertEqual(pi_tc, pi)
            pi_tc_scc = top_cover(friend_matrix, pref_to_cc_method=largest_scc_from_pref)
            self.assertEqual(pi_tc_scc, pi)

        friend_matrix = find_friends(votes, selective_friends=True)
        with open('data/partitions_friends_selective_1_runs.txt', 'w') as f:
            pi = stable_friends(friend_matrix)
            f.write(str(pi) + '\n')
            print(pi)
            print_partition_stats(pi)

            pi_tc = top_cover(friend_matrix)
            self.assertEqual(pi_tc, pi)
            pi_tc_scc = top_cover(friend_matrix, pref_to_cc_method=largest_scc_from_pref)
            self.assertEqual(pi_tc_scc, pi)


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

        friend_matrix = find_friends([
            [1, 1, 2],
            [3, 1, 3],
            [3, 2, 3],
        ])
        self.assertTrue(1 in friend_matrix[0])
        self.assertTrue(0 in friend_matrix[1])
        self.assertFalse(friend_matrix[2])


    def test_find_friends_with_active_players(self):
        friend_matrix = find_friends([
            [1, 1, 2],
            [2, 1, 2],
            [2, 2, 2],
        ], active_players={1, 2})
        self.assertEqual(friend_matrix[0], None)
        self.assertFalse(friend_matrix[1])
        self.assertFalse(friend_matrix[2])

    def test_stable_friends(self):
        friend_matrix = [{1, 2}, {0}, {0}]
        pi = stable_friends(friend_matrix)
        self.assertEqual(len(pi), 1)
        self.assertTrue(frozenset({0, 1, 2}) in pi)
        pi_tc = top_cover(friend_matrix)
        self.assertEqual(pi, pi_tc)
        pi_tc_scc = top_cover(friend_matrix, pref_to_cc_method=largest_scc_from_pref)
        self.assertEqual(pi_tc_scc, pi)

        friend_matrix = [{1}, {0}, set()]
        pi = stable_friends(friend_matrix)
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({0, 1}) in pi)
        self.assertTrue(frozenset({2}) in pi)
        pi_tc = top_cover(friend_matrix)
        self.assertEqual(pi, pi_tc)
        pi_tc_scc = top_cover(friend_matrix, pref_to_cc_method=largest_scc_from_pref)
        self.assertEqual(pi_tc_scc, pi)

        friend_matrix = [{1}, {}, {0, 1}]
        pi = stable_friends(friend_matrix)
        self.assertEqual(len(pi), 3)
        self.assertTrue(frozenset({0}) in pi)
        self.assertTrue(frozenset({1}) in pi)
        self.assertTrue(frozenset({2}) in pi)
        pi_tc = top_cover(friend_matrix)
        self.assertEqual(pi, pi_tc)
        pi_tc_scc = top_cover(friend_matrix, pref_to_cc_method=largest_scc_from_pref)
        self.assertEqual(pi_tc_scc, pi)


    def test_precalculate_coalitions(self):
        coalition_matrix = precalculate_coalitions([[1, 1, 2]])
        self.assertEqual(len(coalition_matrix), 1)
        self.assertEqual(len(coalition_matrix[0]), 3)
        self.assertEqual(coalition_matrix[0][0], {0, 1})
        self.assertEqual(coalition_matrix[0][1], {0, 1})
        self.assertEqual(coalition_matrix[0][2], {2})

        coalition_matrix = precalculate_coalitions([[3, 1, 3]])
        self.assertEqual(len(coalition_matrix), 1)
        self.assertEqual(len(coalition_matrix[0]), 3)
        self.assertEqual(coalition_matrix[0][0], None)
        self.assertEqual(coalition_matrix[0][1], {1})
        self.assertEqual(coalition_matrix[0][2], None)

        coalition_matrix = precalculate_coalitions([
            [1, 1, 2],
            [2, 1, 2],
        ])
        self.assertEqual(len(coalition_matrix), 2)
        self.assertEqual(coalition_matrix[1][0], {0, 2})
        self.assertEqual(coalition_matrix[1][1], {1})
        self.assertEqual(coalition_matrix[1][2], {0, 2})


if __name__ == '__main__':
    unittest.main()
