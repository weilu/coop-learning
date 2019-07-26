import random
import logging
from top_covering import build_graph, find_smallest_cc
from votes_to_game import value_function, get_coalition, majority


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def precalculate_valuations_and_coalitions(S):
    winning_votes = list(map(majority, S))
    value_matrix = []
    coalition_matrix = []
    for row_index, row in enumerate(S):
        winning_vote = winning_votes[row_index]
        values = []
        coalitions = []
        for col_index, vote in enumerate(row):
            values.append(value_function(col_index, row, winning_vote, participation=True))
            coalitions.append(get_coalition(col_index, row, winning_vote))
        value_matrix.append(values)
        coalition_matrix.append(coalitions)
    return value_matrix, coalition_matrix


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
        max_arg = None
        for row_index in S_prime_indexes:
            value = value_matrix[row_index][i]
            if value > max_value:
                max_value = value
                max_arg = row_index
        if max_arg == None:
            B[i] = {i} # checking if i in B doesn't seem to make a difference with the knesset dataset
        else:
            coalition = coalition_matrix[max_arg][i]
            coalition &= players # coalition_matrix always contains the full set of players
            if i not in B: # initialization round
                B[i] = coalition
            else:
                B[i] &= coalition
        logging.debug(f'{i}, {max_value}, {B[i]}')
