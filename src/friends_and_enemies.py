import numpy as np
import logging
import random
from graph_tool.all import *
from top_covering import smallest_cc_from_pref


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def stable_friends(friend_matrix):
    stable_partition = set()
    graph = build_graph(friend_matrix)
    vertex_indexes = graph.vertex_index.copy()
    while(list(graph.vertices())):
        largest_scc = find_largest_scc(graph)
        largest_scc_indexes = frozenset(vertex_indexes[v] for v in largest_scc)
        # print('largest_scc:', largest_scc_indexes)
        stable_partition.add(largest_scc_indexes)
        friend_matrix = update_friend_matrix(friend_matrix, largest_scc_indexes)
        graph.remove_vertex(largest_scc)

    return stable_partition


def build_graph(friend_matrix):
    g = Graph()
    g.add_vertex(len(friend_matrix))
    for i, friends in enumerate(friend_matrix):
        if friends is None:
            continue
        g.add_edge(i, i) # add edge to self
        for friend in friends:
            g.add_edge(i, friend)
    return g


def find_largest_scc(graph):
    scc_graph = graph_tool.topology.extract_largest_component(graph)
    return list(scc_graph.vertices())


def update_friend_matrix(friend_matrix, to_remove):
    updated_friend_matrix = friend_matrix.copy()
    for i, friends in enumerate(friend_matrix):
        if i in to_remove:
            updated_friends = None
        elif friends is None:
            continue
        else:
            updated_friends = friends - to_remove
        updated_friend_matrix[i] = updated_friends
    return updated_friend_matrix


def precalculate_frenemy_per_player_per_bill(votes):
    num_bills = len(votes)
    num_players = len(votes[0])
    diff_matrix = np.zeros((num_bills, num_players, num_players))
    for my_index in range(num_players):
        for row_index, row in enumerate(votes):
            my_vote = row[my_index]
            if my_vote not in {1, 2}:
                continue
            for col_index, vote in enumerate(row):
                if vote not in {1, 2}:
                    continue
                if col_index != my_index:
                    if vote == my_vote:
                        diff_matrix[row_index, my_index, col_index] += 1
                    else:
                        diff_matrix[row_index, my_index, col_index] -= 1
    return diff_matrix


def find_friends(votes, active_players=None):
    diff_matrix = precalculate_frenemy_per_player_per_bill(votes)
    return find_friends_from_sample(list(range(len(votes))), diff_matrix, active_players)


def find_friends_from_sample(sample_bill_indexes, diff_matrix, active_players=None):
    num_players = len(diff_matrix[0, 0])

    diff_matrix = diff_matrix[sample_bill_indexes]
    frenemy_matrix = np.sum(diff_matrix, axis=0)

    friend_matrix = []
    for i, row in enumerate(frenemy_matrix):
        if active_players and i not in active_players:
            friend_matrix.append(None)
        else:
            friends = set([i for i, count in enumerate(row) if count > 0])
            if active_players:
                friends &= active_players
            friend_matrix.append(friends)
    return friend_matrix


# top cover needs to be re-implemented to avoid having to expand the full preference profile
def top_cover(friend_matrix):
    stable_partition = set()
    pref = to_choice_sets(friend_matrix)
    while pref.keys():
        smallest_cc = smallest_cc_from_pref(pref)
        stable_partition.add(smallest_cc)
        friend_matrix = update_friend_matrix(friend_matrix, smallest_cc)
        pref = to_choice_sets(friend_matrix)
    return stable_partition


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


def to_choice_sets(friend_matrix):
    choice_sets = {}
    for i, friends in enumerate(friend_matrix):
        if friends is not None:
            choice_sets[i] = [friends]
    return choice_sets


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


def approximate_preferences(votes, B, players, diff_matrix, sample_size, sample_method):
    S_prime_indexes = sample_method(range(len(votes)), k=sample_size)
    sample_votes = list(votes[i] for i in S_prime_indexes)
    logging.info('start finding friends')
    friend_matrix = find_friends_from_sample(S_prime_indexes, diff_matrix, active_players=players)
    logging.info('done finding friends')
    for i in range(len(sample_votes[0])):
        if i not in players:
            continue
        if i in B and B[i] == {i}: # already singleton, no need to check further
            continue
        max_count = 0
        max_coalition = None
        for bill in sample_votes:
            my_vote = bill[i]
            if my_vote not in {1, 2}:
                continue
            voted_with_me = set()
            for col_index, vote in enumerate(bill):
                if vote == my_vote:
                    voted_with_me.add(col_index)
            friends_voted_with_me = voted_with_me & friend_matrix[i]
            if len(friends_voted_with_me) > max_count:
                max_count = len(friends_voted_with_me)
                max_coalition = voted_with_me
        old_coal_len = len(B[i]) if i in B else 0
        if max_coalition == None:
            B[i] = {i}
        else:
            if i not in B: # initialization round
                B[i] = max_coalition
            else:
                B[i] &= max_coalition
        if old_coal_len != len(B[i]):
            logging.info(f'{i} coalition size reduced: {old_coal_len} -> {len(B[i])}')


def pac_top_cover(votes, sample_size=None, sample_method=random.choices):
    if sample_size is None:
        sample_size = len(votes)

    players = set(range(len(votes[0])))
    stable_partition = set()

    diff_matrix = precalculate_frenemy_per_player_per_bill(votes)
    while players:
        logging.info(f'{len(players)} players left')
        B = {}
        approximate_preferences(votes, B, players, diff_matrix, sample_size, sample_method)
        # successive restriction loop
        for round_index in range(len(players)):
            logging.info(f'round {round_index}')
            approximate_preferences(votes, B, players, diff_matrix, sample_size, sample_method)
        logging.debug(f'done approximating preferences')

        smallest_cc = smallest_cc_from_pref(B)
        stable_partition.add(smallest_cc)
        logging.debug(f'done finding smallest cc')

        players = players - smallest_cc

    return stable_partition
