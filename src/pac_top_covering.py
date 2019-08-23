import random
import logging
from top_covering import smallest_cc_from_pref
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

        if w != None: # w = None means no sampling
            # successive restriction loop
            for round_index in range(len(players)):
                logging.info(f'round {round_index}')
                approximate_preferences(players, S, B, value_matrix, coalition_matrix, w)
        logging.debug(f'done approximating preferences')

        # perform top covering
        smallest_cc = smallest_cc_from_pref(B)
        stable_partition.add(smallest_cc)
        logging.info(f'players to remove: {smallest_cc}')

        players = players - smallest_cc
        # remove coalitions with removed players
        for i, row in enumerate(coalition_matrix):
            for j, coalition in enumerate(row):
                if coalition is not None and (coalition - players):
                    coalition_matrix[i][j] = None
                    value_matrix[i][j] = 0

    return stable_partition


def approximate_preferences(players, S, B, value_matrix, coalition_matrix, w):
    if w == None: # no sampling, useful for testing
        w = len(S)
        S_prime_indexes = range(len(S))
    else:
        S_prime_indexes = random.choices(range(len(S)), k=w) # with replacement
    for i in players:
        if i in B and B[i] == {i}: # already singleton, no need to check further
            continue
        max_value = 0
        max_coalition = None
        for row_index in S_prime_indexes:
            coalition = coalition_matrix[row_index][i]
            if coalition is None:
                continue
            value = value_matrix[row_index][i]
            if value > max_value:
                max_value = value
                max_coalition = coalition
        old_coal_len = len(B[i]) if i in B else 0
        if max_coalition == None:
            B[i] = {i} # checking if i in B doesn't seem to make a difference with the knesset dataset
        else:
            if i not in B: # initialization round
                B[i] = max_coalition
            else:
                B[i] &= max_coalition
        if old_coal_len != len(B[i]):
            logging.info(f'player {i}\'s coalition size changed: {old_coal_len} -> {len(B[i])}. {B[i]}')
        logging.debug(f'{i}, {max_value}, {B[i]}')
