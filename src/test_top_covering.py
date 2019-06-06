import unittest
import random
import itertools
from top_covering import top_cover


class TestTopCovering(unittest.TestCase):

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
        self.assertEqual(pi[0], frozenset({1, 2, 3}))
        self.assertEqual(pi[1], frozenset({4}))

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
        self.assertEqual(pi[0], frozenset({1, 2, 3}))
        self.assertEqual(pi[1], frozenset({4, 5}))

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
        self.assertEqual(pi[0], frozenset({1, 2, 3, 4, 5, 6}))

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
        self.assertEqual(pi[0], frozenset({1, 2, 3}))
        self.assertEqual(pi[1], frozenset({4, 5}))
        self.assertEqual(pi[2], frozenset({6}))


def check_top_responsive(game):
    pass #TODO

def check_stable(game, partition):
    pass #TODO

def generate_preference_ranking(i, num_players):
    ranking = [j for j in range(1, i)] + [j for j in range(i+1, num_players+1)]
    random.shuffle(ranking)
    ranking.append(i) # TODO: Does a player have to prefer him/herself last?
    return ranking

def generate_b_hedonic_game(num_players, seed):
    random.seed(seed)
    for i in range(1, num_players+1):
        ranking = generate_preference_ranking(i, num_players)
        print(ranking)
        extended_ranking = []
        for j in range(0, len(ranking)):
            extended_ranking += extend_ranking(i, ranking[j:])
        print(extended_ranking)

def extend_ranking(i, ranking):
    if ranking[0] == i: # top preference is self
        return [{i}]

    ranking_copy = ranking.copy()
    ranking_copy.remove(i) # remove self
    top_choice = ranking_copy.pop(0)
    subset = {i, top_choice}
    extended_ranking = [subset]

    for size in range(1, len(ranking_copy)+1):
        # for any given size, player i is indifferent as long as the subset is fixed
        # but we use a list so the tie is arbitrarily broken in practice
        for filler in itertools.combinations(ranking_copy, size):
            extended_ranking.append(subset | set(filler))

    return extended_ranking


if __name__ == '__main__':
    # unittest.main()
    generate_b_hedonic_game(4, 1337)
