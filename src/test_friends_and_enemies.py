import copy
import random
import unittest
from knesset_test import print_partition_stats, calculate_partition_edit_distances_and_print_stats
from friends_and_enemies import stable_friends, find_friends, top_cover, to_avoid_sets, bottom_avoid, pac_top_cover, precalculate_coalitions
from top_covering import largest_scc_from_pref
from partition_ids_to_names import build_member_map, partition_id_str_to_names
from votes_to_game import partition_edit_distance, read_votes_and_player_data


class TestFriendsAndEnemies(unittest.TestCase):

    def test_pac_top_cover(self):
        votes = [
            [1, 1, 2],
        ]
        pi = pac_top_cover(votes, sample_method=random.sample)
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({0, 1}) in pi)
        self.assertTrue(frozenset({2}) in pi)

        votes = [
            [1, 1, 2],
            [2, 1, 2],
            [2, 2, 2],
        ]
        pi = pac_top_cover(votes, sample_method=random.sample)
        self.assertEqual(len(pi), 1)
        self.assertTrue(frozenset({0, 1, 2}) in pi)

        votes = [
            [1, 1, 2],
            [3, 1, 3],
            [3, 2, 3],
        ]
        pi = pac_top_cover(votes, sample_method=random.sample)
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({0, 1}) in pi)
        self.assertTrue(frozenset({2}) in pi)


    def test_pac_knesset(self):
        member_map = build_member_map()
        random.seed(42)
        partitions = []
        original_votes, _ = read_votes_and_player_data()
        sample_size = int(0.75 * len(original_votes))
        for _ in range(50):
            votes = copy.deepcopy(original_votes)
            pi = pac_top_cover(votes, sample_size)
            print(pi)
            print_partition_stats(pi)
            partition_id_str_to_names(str(pi), member_map)
            partitions.append(pi)

        calculate_partition_edit_distances_and_print_stats(partitions)


    def test_knesset(self):
        votes, player_labels = read_votes_and_player_data()
        friend_matrix = find_friends(votes)
        pi = stable_friends(friend_matrix)
        print(pi)
        print_partition_stats(pi)
        # TODO: verify core stable
        pi_tc = top_cover(friend_matrix)
        self.assertEqual(pi_tc, pi)
        pi_tc_scc = top_cover(friend_matrix, pref_to_cc_method=largest_scc_from_pref)
        self.assertEqual(pi_tc_scc, pi)

        pi_ba = bottom_avoid(friend_matrix)
        print(pi_ba)
        print_partition_stats(pi_ba)
        # TODO: verify core stable

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
