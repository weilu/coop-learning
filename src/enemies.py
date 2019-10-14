import copy
import logging
import random
from friends import update_friend_matrix, precalculate_frenemy_per_player_per_bill, find_friends_from_sample

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def bottom_avoid(friend_matrix):
    stable_partition = set()
    pref = to_avoid_sets(friend_matrix)
    while pref.keys():
        coalition = remove_bottom_players(pref, friend_matrix)
        stable_partition.add(coalition)
        friend_matrix = update_friend_matrix(friend_matrix, coalition)
        pref = to_avoid_sets(friend_matrix)

    return stable_partition


def remove_bottom_players(pref, friend_matrix):
    for i, least_preferred in pref.items():
        if not least_preferred:
            continue
        if least_preferred != {i}:
            to_remove = set(least_preferred - {i}).pop()
            friend_matrix = update_friend_matrix(friend_matrix, {to_remove})
            pref = to_avoid_sets(friend_matrix)
            return remove_bottom_players(pref, friend_matrix)
    return frozenset(pref.keys())


def to_avoid_sets(friend_matrix):
    active_players = set()
    for i, friends in enumerate(friend_matrix):
        if friends is not None:
            active_players.add(i)

    avoid_sets = {}
    for i, friends in enumerate(friend_matrix):
        if friends is not None:
            avoid_sets[i] = active_players - friends
    return avoid_sets


def approximate_friends(votes, players, diff_matrix, sample_size, sample_method):
    S_prime_indexes = sample_method(range(len(votes)), k=sample_size)
    friend_matrix = find_friends_from_sample(S_prime_indexes, diff_matrix, active_players=players)
    return friend_matrix


def pac_bottom_avoid(votes, diff_matrix, sample_size, sample_method=random.choices):
    num_players = len(votes[0])
    players = set(range(num_players))
    stable_partition = set()

    while players:
        logging.info(f'{len(players)} players left')
        B = {}
        friend_matrix = approximate_friends(votes, players, diff_matrix, sample_size, sample_method)
        # successive restriction loop
        for round_index in range(len(players)):
            logging.debug(f'round {round_index}')
            new_friend_matrix = approximate_friends(votes, players, diff_matrix, sample_size, sample_method)
            logging.debug(f'done approximating friends')
            # take intersection of friends across samples
            for i, row in enumerate(new_friend_matrix):
                if row is None:
                    continue
                friend_matrix[i] &= row
            logging.debug(f'done updating friends')

        pref = to_avoid_sets(friend_matrix)
        coalition = remove_bottom_players(pref, friend_matrix)
        stable_partition.add(coalition)
        players = players - coalition

    return stable_partition
