import random
import itertools


def check_top_responsive(game):
    all_subsets = get_all_subsets(game.keys())
    for i, preferences in game.items():
        subsets_with_i = list(filter(lambda s: i in s, all_subsets))
        for si in range(0, len(subsets_with_i)-1):
            s = subsets_with_i[si]
            cs_s = get_choice_set(preferences, s)
            for ti in range(si+1, len(subsets_with_i)):
                t = subsets_with_i[ti]
                cs_t = get_choice_set(preferences, t)

                if preferences.index(cs_s) < preferences.index(cs_t):
                    assert preferences.index(s) < preferences.index(t), \
                            f'Player {i}, CS_S: {cs_s} > CS_T: {cs_t}, expect S: {s} > T: {t}, but not the case.\n Game: {game}'
                elif preferences.index(cs_t) < preferences.index(cs_s):
                    assert preferences.index(t) < preferences.index(s), \
                            f'Player {i}, CS_S: {cs_s} < CS_T: {cs_t}, expect S: {s} < T: {t}, but not the case.\n Game: {game}'
                else:
                    if s < t:
                        assert preferences.index(s) < preferences.index(t), \
                            f'Player {i}, CS_S: {cs_s} = CS_T: {cs_t}, s in t, expect S: {s} > T: {t}, but not the case.\n Game: {game}'
                    elif t < s:
                        assert preferences.index(t) < preferences.index(s), \
                            f'Player {i}, CS_S: {cs_s} = CS_T: {cs_t}, t in s, expect S: {t} > T: {s}, but not the case.\n Game: {game}'

def get_choice_set(preferences, available_players):
    for players in preferences:
        if all(j in available_players for j in players):
            return players

def get_all_subsets(available_players):
    all_subsets = set()
    for size in range(1, len(available_players)+1):
        for subset in itertools.combinations(available_players, size):
            all_subsets.add(frozenset(subset))
    return all_subsets


def check_stable(game, partition):
    for i, preferences in game.items():
        coalition = get_coalition(i, partition)
        for better_coalition_index in range(0, preferences.index(coalition)):
            better_coalition = preferences[better_coalition_index]
            other_players = better_coalition - {i}
            better_for_all = all(better_off(game[j], better_coalition, get_coalition(j, partition)) for j in other_players)
            if better_for_all:
                return False
    return True

# can be optimized to avoid repeatedly finding containing coalition
def get_coalition(i, partition):
    for subset in partition:
        if i in subset:
            return subset

def better_off(preferences, better_coalition, coalition):
    return preferences.index(better_coalition) < preferences.index(coalition)


def generate_preference_ranking(i, num_players):
    ranking = [j for j in range(1, i)] + [j for j in range(i+1, num_players+1)]
    random.shuffle(ranking)
    ranking.append(i) # TODO: Does a player have to prefer him/herself last?
    return ranking

def generate_b_hedonic_game(num_players, seed=None):
    if seed:
        random.seed(seed)

    game = {}
    for i in range(1, num_players+1):
        ranking = generate_preference_ranking(i, num_players)
        extended_ranking = []
        for j in range(0, len(ranking)):
            extended_ranking += extend_ranking(i, ranking[j:])
        game[i] = extended_ranking
    return game

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
    game = generate_b_hedonic_game(4)
    check_top_responsive(game)
