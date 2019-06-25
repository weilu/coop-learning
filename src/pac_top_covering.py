import random
from top_covering import build_graph, find_smallest_cc
from votes_to_game import value_function, get_coalition


def pac_top_cover(players, S):
    stable_partition = set()
    w = len(S) # TODO: Proper calculation
    while players:
        S_prime = random.choices(S, k=w) # with replacement
        # S_prime = S
        # print(S_prime)
        B = {}
        for i in players:
            max_value = 0
            max_arg = None
            for T in S_prime:
                value = value_function(i, T)
                print(i, value, T)
                if value > max_value:
                    max_value = value
                    max_arg = T
            if not max_arg:
                B[i] = {i}
            else:
                B[i] = get_coalition(i, max_arg)
        # print(B)
        #TODO: successive restriction loop
        graph, vlabel_to_index = build_graph(B)
        smallest_cc = find_smallest_cc(graph)
        stable_partition.add(smallest_cc)
        players = players - smallest_cc
        for row in S:
            for index, el in enumerate(row):
                if index in smallest_cc:
                    row[index] = None
    print(stable_partition)
    return stable_partition

