import random
from top_covering import build_graph, find_smallest_cc
from votes_to_game import value_function, get_coalition


def pac_top_cover(players, S):
    stable_partition = set()
    w = len(S) # TODO: Proper calculation
    while players:
        B = {}
        approximate_preferences(players, S, B)

        # successive restriction loop
        for _ in range(len(players)):
            approximate_preferences(players, S, B)

        # perform top covering
        graph, vlabel_to_index = build_graph(B)
        smallest_cc = find_smallest_cc(graph)
        stable_partition.add(smallest_cc)
        players = players - smallest_cc
        for row in S:
            for index, el in enumerate(row):
                if index in smallest_cc:
                    row[index] = None

    return stable_partition


def approximate_preferences(players, S, B):
    # S_prime = random.choices(S, k=w) # with replacement
    S_prime = S # TODO: stub this for testing
    for i in players:
        max_value = 0
        max_arg = None
        for T in S_prime:
            value = value_function(i, T)
            if value > max_value:
                max_value = value
                max_arg = T
        if not max_arg:
            B[i] = {i}
        else:
            coalition = get_coalition(i, max_arg)
            if i not in B: # initialization round
                B[i] = coalition
            else:
                B[i] &= coalition
