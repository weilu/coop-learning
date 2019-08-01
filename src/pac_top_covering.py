import random
import logging
from top_covering import build_graph, find_smallest_cc
from votes_to_game import value_function, get_coalition, majority, precalculate_valuations_and_coalitions


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def pac_top_cover(num_players, S, w=None):
    players = set(range(num_players))
    stable_partition = set()

    logging.info(f'Start calculating valuations & coalitions')
    value_matrix, coalition_matrix = precalculate_valuations_and_coalitions(S)
    logging.info(f'Done calculating valuations & coalitions')

    while players:
        logging.info(f'{len(players)} players left')
        B = {}
        approximate_preferences(players, S, B, value_matrix, coalition_matrix, w)

        # if w != None: # w = None means no sampling
        #     # successive restriction loop
        #     for _ in range(len(players)):
        #         approximate_preferences(players, S, B, value_matrix, coalition_matrix, w)
        logging.debug(f'done approximating preferences')

        # perform top covering
        graph, vlabel_to_index = build_graph(B)
        smallest_cc = find_smallest_cc(graph)
        stable_partition.add(smallest_cc)
        logging.debug(f'done finding smallest cc')

        players = players - smallest_cc

    return stable_partition


def approximate_preferences(players, S, B, value_matrix, coalition_matrix, w):
    if w == None: # no sampling, useful for testing
        w = len(S)
        S_prime_indexes = range(len(S))
    else:
        S_prime_indexes = random.choices(range(len(S)), k=w) # with replacement
    for i in players:
        max_value = 0
        max_coalition = None
        for row_index in S_prime_indexes:
            coalition = coalition_matrix[row_index][i]
            if coalition - players:
                continue
            value = value_matrix[row_index][i]
            if value > max_value:
                max_value = value
                max_coalition = coalition
        if max_coalition == None:
            B[i] = {i} # checking if i in B doesn't seem to make a difference with the knesset dataset
        else:
            if i not in B: # initialization round
                B[i] = max_coalition
            else:
                B[i] &= max_coalition
        logging.debug(f'{i}, {max_value}, {B[i]}')
