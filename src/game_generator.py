import random
import itertools
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def check_top_responsive(game, return_violations=False):
    # only check known subsets, as the all-subset space could be very big
    game = freeze(game)
    all_subsets = set()
    for row in game.values():
        for subset in row:
            all_subsets.add(subset)

    violations = []
    for i, preferences in game.items():
        logging.info(f'checking player {i}')
        subsets_with_i = list(filter(lambda s: i in s, all_subsets))
        for si in range(0, len(subsets_with_i)-1):
            s = subsets_with_i[si]
            cs_s = get_choice_set(preferences, s)
            for ti in range(si+1, len(subsets_with_i)):
                t = subsets_with_i[ti]
                cs_t = get_choice_set(preferences, t)

                if preferences.index(cs_s) < preferences.index(cs_t):
                    if not preferences.index(s) < preferences.index(t):
                        violations.append(f'Player {i}, CS_S: {cs_s} > CS_T: {cs_t}, expect S: {s} > T: {t}, but not the case.\n Game: {game}')
                elif preferences.index(cs_t) < preferences.index(cs_s):
                    if not preferences.index(t) < preferences.index(s):
                        violations.append(f'Player {i}, CS_S: {cs_s} < CS_T: {cs_t}, expect S: {s} < T: {t}, but not the case.\n Game: {game}')
                else:
                    if s < t:
                        if not preferences.index(s) < preferences.index(t):
                            violations.append(f'Player {i}, CS_S: {cs_s} = CS_T: {cs_t}, s in t, expect S: {s} > T: {t}, but not the case.\n Game: {game}')
                    elif t < s:
                        if not preferences.index(t) < preferences.index(s):
                            violations.append(f'Player {i}, CS_S: {cs_s} = CS_T: {cs_t}, t in s, expect S: {t} > T: {s}, but not the case.\n Game: {game}')

                if not return_violations and violations:
                    assert False, violations[0]

        logging.info(f'found {len(violations)} violations')

    if return_violations:
        return (len(violations) == 0), violations
    else:
        return True


def get_choice_set(preferences, available_players):
    for players in preferences:
        if all(j in available_players for j in players):
            return players


# incomplete core stability check – only checking against known coalitions explicitly listed in preferences
def check_core_stable(game, partition, return_better=False):
    coalition_map = partition_to_coalition_map(partition)
    for i, preferences in game.items():
        coalition = coalition_map[i]
        end_index = len(preferences) if coalition not in preferences else preferences.index(coalition)
        for better_coalition_index in range(0, end_index):
            better_coalition = preferences[better_coalition_index]
            other_players = better_coalition - {i}
            better_for_all = all(better_off(game[j], better_coalition, coalition_map[j]) for j in other_players)
            if better_for_all:
                if return_better:
                    return False, better_coalition
                else:
                    return False
    if return_better:
        return True, {}
    else:
        return True

def partition_to_coalition_map(partition):
    coalition_map = {}
    for part in partition:
        for player in part:
            coalition_map[player] = part
    return coalition_map

def better_off(preferences, better_coalition, coalition):
    if better_coalition in preferences and coalition in preferences:
        return preferences.index(better_coalition) < preferences.index(coalition)
    elif better_coalition in preferences:
        return True
    else:
        return False

def search_stable_partition(game):
    pi = [frozenset(game.keys())]
    is_stable = False
    while not is_stable:
        is_stable, better_coalition = check_core_stable(game, pi, return_better=True)
        if is_stable:
            break
        new_pi = [frozenset(better_coalition)]
        for coal in pi:
            if coal & better_coalition:
                remain = coal - better_coalition
                if remain:
                    new_pi.append(frozenset(remain))
            else:
                new_pi.append(coal)
        pi = new_pi
    return pi


def generate_preference_ranking(i, num_players):
    ranking = [j for j in range(1, i)] + [j for j in range(i+1, num_players+1)]
    random.shuffle(ranking)
    ranking.append(i) # A player prefer him/herself last. It's not a requirement of B hedonic games
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


def freeze(pref):
    frozen = {}
    for k, v in pref.items():
        frozen[k] = [frozenset(neighbors) for neighbors in v]
    return frozen


if __name__ == '__main__':
    game = generate_b_hedonic_game(4)
    check_top_responsive(game)
