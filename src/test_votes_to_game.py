import unittest
from votes_to_game import majority, value_function, get_coalition, value_matrix_to_preferences


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
        self.assertEqual(game[0], [{0, 1, 2, 3}, {0}])
        self.assertEqual(game[1], [{0, 1, 2, 3}, {1}])
        self.assertEqual(game[2], [{2, 3}, {0, 1, 2, 3}])
        self.assertEqual(game[3], [{2, 3}, {0, 1, 2, 3}])


if __name__ == '__main__':
    unittest.main()
