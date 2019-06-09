import unittest
from game_generator import get_all_subsets, get_choice_set, check_top_responsive


class TestGameGenerator(unittest.TestCase):

    def test_get_all_subsets(self):
        subsets = get_all_subsets({1, 2, 3, 4})
        self.assertEqual(len(subsets), 15)
        self.assertEqual(len(list(filter(lambda s: len(s) == 1, subsets))), 4)
        self.assertEqual(len(list(filter(lambda s: len(s) == 2, subsets))), 6)
        self.assertEqual(len(list(filter(lambda s: len(s) == 3, subsets))), 4)
        self.assertEqual(len(list(filter(lambda s: len(s) == 4, subsets))), 1)

    def test_get_choice_set(self):
        cs = get_choice_set([{1}, {1, 2}, {1, 3}, {1, 2, 3}], {1, 2, 3})
        self.assertEqual(cs, {1})

        cs = get_choice_set([{1, 2}, {1, 3}, {1, 2, 3}, {1}], {1, 2, 3})
        self.assertEqual(cs, {1, 2})

        cs = get_choice_set([{1, 2}, {1, 3}, {1, 2, 3}, {1}], {1, 3})
        self.assertEqual(cs, {1, 3})

    def test_check_top_responsive(self):
        game = {
            1: [{1, 2}, {1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 3}, {1, 3, 4}, {1, 4}, {1}],
            2: [{2, 3}, {2, 3, 4}, {1, 2, 3}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 2}, {2}],
            3: [{1, 3}, {1, 2, 3}, {1, 3, 4}, {1, 2, 3, 4}, {2, 3}, {2, 3, 4}, {3, 4}, {3}],
            4: [{3, 4}, {2, 3, 4}, {1, 3, 4}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 4}, {4}]
        }
        check_top_responsive(game)

        game = {
            1: [{1, 2}, {1, 2, 3}, {1, 3}, {1}],
            2: [{2, 3}, {1, 2, 3}, {2, 1}, {2}],
            3: [{1, 3}, {1, 2, 3}, {2, 3}, {3}]
        }

        check_top_responsive(game)

        game = {
            1: [{1, 2}, {1, 3}, {1, 2, 3}, {1}],
            2: [{2, 3}, {1, 2, 3}, {2, 1}, {2}],
            3: [{1, 3}, {1, 2, 3}, {2, 3}, {3}]
        }
        self.assertRaises(AssertionError, check_top_responsive, game)


if __name__ == '__main__':
    unittest.main()
