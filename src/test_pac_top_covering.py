import unittest
from pac_top_covering import pac_top_cover
from top_covering import top_cover
from votes_to_game import precalculate_valuations_and_coalitions, value_matrix_to_preferences


class TestPacTopCovering(unittest.TestCase):

    def test_simple(self):
        votes = [[1, 1, 1, 2, 2, 2, 1],
                 [1, 1, 1, 2, 2, 2, 2], ]
        pi = pac_top_cover(7, votes)

        self.assertEqual(len(pi), 4)
        self.assertTrue(frozenset({0, 1, 2, 6}) in pi)
        self.assertTrue(frozenset({3}) in pi)
        self.assertTrue(frozenset({4}) in pi)
        self.assertTrue(frozenset({5}) in pi)

        value_matrix, coalition_matrix = precalculate_valuations_and_coalitions(votes)
        game = value_matrix_to_preferences(value_matrix, coalition_matrix)
        pi_top = top_cover(game)

        self.assertEqual(pi, set(pi_top))


    def test_simpler(self):
        votes = [[1, 1, 2, 2],
                 [1, 1, 1, 1], ]
        pi = pac_top_cover(4, votes)

        self.assertEqual(len(pi), 3)
        self.assertTrue(frozenset({0}) in pi)
        self.assertTrue(frozenset({1}) in pi)
        self.assertTrue(frozenset({2, 3}) in pi)

        value_matrix, coalition_matrix = precalculate_valuations_and_coalitions(votes)
        game = value_matrix_to_preferences(value_matrix, coalition_matrix)
        pi_top = top_cover(game)

        self.assertEqual(pi, set(pi_top))


    def test_remove_player(self):
        votes = [[1, 1, 2, 2],
                 [1, 1, 1, 1],
                 [1, 2, 2, 2],
                 [2, 2, 0, 0]]
        pi = pac_top_cover(4, votes)

        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset({0, 1}) in pi)
        self.assertTrue(frozenset({2, 3}) in pi)

        value_matrix, coalition_matrix = precalculate_valuations_and_coalitions(votes)
        game = value_matrix_to_preferences(value_matrix, coalition_matrix)
        pi_top = top_cover(game)

        self.assertEqual(pi, set(pi_top))


if __name__ == '__main__':
    unittest.main()
