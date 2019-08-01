import unittest
import itertools
from top_covering import top_cover, find_smallest_cc
from game_generator import generate_b_hedonic_game, check_core_stable


class TestTopCovering(unittest.TestCase):

    def test_find_smallest_cc(self):
        pass

    # Example 15.5, Handbook of Computational Social Choice, p365
    # https://doi.org/10.1017/CBO9781107446984.016
    def test_simple(self):
        sample = {
            1: [{1, 2}, {1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 3}, {1, 3, 4}, {1, 4}, {1}],
            2: [{2, 3}, {2, 3, 4}, {1, 2, 3}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 2}, {2}],
            3: [{1, 3}, {1, 2, 3}, {1, 3, 4}, {1, 2, 3, 4}, {2, 3}, {2, 3, 4}, {3, 4}, {3}],
            4: [{3, 4}, {2, 3, 4}, {1, 3, 4}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 4}, {4}]
        }
        pi = top_cover(sample)
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({1, 2, 3}) in pi)
        self.assertTrue(frozenset({4}) in pi)

    def test_simple_modified(self):
        sample = {
            1: [{1, 2}, {1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 3}, {1, 3, 4}, {1, 4}, {1}],
            2: [{2, 3}, {2, 3, 4}, {1, 2, 3}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 2}, {2}],
            3: [{1, 3}, {1, 2, 3}, {1, 3, 4}, {1, 2, 3, 4}, {2, 3}, {2, 3, 4}, {3, 4}, {3}],
            4: [{3, 4}, {4, 5}, {4}],
            5: [{4, 5}, {5}]
        }
        pi = top_cover(sample)
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({1, 2, 3}) in pi)
        self.assertTrue(frozenset({4, 5}) in pi)

    def test_all_in_one(self):
        sample = {
            1: [{1, 2}],
            2: [{2, 3, 6}],
            3: [{1, 3}],
            4: [{3, 4, 5}],
            5: [{4, 5, 6}],
            6: [{4, 6}],
        }
        pi = top_cover(sample)
        self.assertEqual(len(pi), 1)
        self.assertTrue(frozenset({1, 2, 3, 4, 5, 6}) in pi)

    def test_multiple_iteration(self):
        sample = {
            1: [{1, 2}],
            2: [{2, 3}, {2, 6}],
            3: [{1, 3}],
            4: [{3, 4}, {4, 5}],
            5: [{4, 5}, {5, 6}],
            6: [{4, 6}],
        }
        pi = top_cover(sample)
        self.assertEqual(len(pi), 3)
        self.assertTrue(frozenset({1, 2, 3}) in pi)
        self.assertTrue(frozenset({4, 5}) in pi)
        self.assertTrue(frozenset({6}) in pi)

    def test_generated_b_games(self):
        for size in range(2, 7):
            for seed in range(10):
                game = generate_b_hedonic_game(size, seed)
                pi = top_cover(game)
                self.assertTrue(check_core_stable(game, pi))

    def test_three_players(self):
        sample = {
            1: [{1, 2}, {1, 2, 3}, {1}, {1, 3}],
            2: [{2, 3}, {1, 2, 3}, {2}, {1, 2}],
            3: [{1, 3}, {1, 2, 3}, {3}, {2, 3}],
        }
        pi = top_cover(sample)
        self.assertEqual(len(pi), 1)
        self.assertTrue(frozenset({1, 2, 3}) in pi)

    def test_seven_players(self):
        all_players = {1, 2, 3, 4, 5, 6, 7}

        player_1_pref = expand_preferences({1, 2}, all_players, [])
        expand_preferences({1}, all_players, player_1_pref)

        player_2_pref = expand_preferences({2, 3}, all_players, [])
        expand_preferences({2}, all_players, player_2_pref)

        player_3_pref = expand_preferences({3, 1}, all_players - {7}, [])
        expand_preferences({3, 7}, all_players, player_3_pref)
        expand_preferences({3}, all_players, player_3_pref)

        player_4_pref = expand_preferences({4, 5}, all_players, [])
        expand_preferences({4}, all_players, player_4_pref)

        player_5_pref = expand_preferences({5, 6}, all_players, [])
        expand_preferences({5}, all_players, player_5_pref)

        player_6_pref = expand_preferences({6, 4}, all_players - {1}, [])
        expand_preferences({6, 1}, all_players, player_6_pref)
        expand_preferences({6}, all_players, player_6_pref)

        player_7_pref = expand_preferences({7, 4}, all_players, [])
        expand_preferences({7}, all_players, player_7_pref)

        sample = {
            1: player_1_pref,
            2: player_2_pref,
            3: player_3_pref,
            4: player_4_pref,
            5: player_5_pref,
            6: player_6_pref,
            7: player_7_pref,
        }

        pi = top_cover(sample)
        self.assertEqual(len(pi), 3)
        self.assertTrue(frozenset({1, 2, 3}) in pi)
        self.assertTrue(frozenset({4, 5, 6}) in pi)
        self.assertTrue(frozenset({7}) in pi)

    def test_multiple_player_top_sets(self):
        all_players = {1, 2, 3, 4}

        player_1_pref = expand_preferences({1, 2, 3}, all_players, [])
        expand_preferences({1}, all_players, player_1_pref)

        player_2_pref = expand_preferences({2, 1}, all_players, [])
        expand_preferences({2}, all_players, player_2_pref)

        player_3_pref = expand_preferences({3, 4}, all_players - {7}, [])
        expand_preferences({3}, all_players, player_3_pref)

        player_4_pref = expand_preferences({4, 2, 3}, all_players, [])
        expand_preferences({4}, all_players, player_4_pref)

        sample = {
            1: player_1_pref,
            2: player_2_pref,
            3: player_3_pref,
            4: player_4_pref,
        }

        pi = top_cover(sample)
        self.assertEqual(len(pi), 1)
        self.assertTrue(frozenset({1, 2, 3, 4}) in pi)


def expand_preferences(fixed_players, all_players, current_preferences):
    current_preferences.append(fixed_players)
    rest_of_players = all_players - fixed_players
    for size in range(1, len(rest_of_players) + 1):
        for filler in itertools.combinations(rest_of_players, size):
            subset = set(filler) | fixed_players
            if subset not in current_preferences:
                current_preferences.append(subset)
    return current_preferences


if __name__ == '__main__':
    unittest.main()
