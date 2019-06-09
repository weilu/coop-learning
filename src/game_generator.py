import random
import itertools


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
    generate_b_hedonic_game(4, 1337)
