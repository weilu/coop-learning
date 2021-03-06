import copy
import numpy as np
import logging
import random
import time
from graph_tool.all import *
from top_covering import smallest_cc_from_pref, largest_scc_from_pref
from votes_to_game import read_votes_and_player_data


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


def precalculate_frenemy_per_player_per_bill(votes, selective_friends):
    num_bills = len(votes)
    num_players = len(votes[0])
    diff_matrix = np.zeros((num_bills, num_players, num_players))
    for my_index in range(num_players):
        for row_index, row in enumerate(votes):
            my_vote = row[my_index]
            if my_vote not in {1, 2}:
                continue
            for col_index, vote in enumerate(row):
                if selective_friends:
                    effective_vote = True
                else:
                    effective_vote = vote in {1, 2}
                if not effective_vote:
                    continue

                if col_index != my_index:
                    if vote == my_vote:
                        diff_matrix[row_index, my_index, col_index] += 1
                    else:
                        diff_matrix[row_index, my_index, col_index] -= 1
    return diff_matrix


def find_friends(votes, active_players=None, selective_friends=False):
    diff_matrix = precalculate_frenemy_per_player_per_bill(votes, selective_friends)
    if active_players is None:
        active_players = set(range(len(votes[0])))
    return find_friends_from_sample(list(range(len(votes))), diff_matrix, active_players)


def find_friends_from_sample(sample_bill_indexes, diff_matrix, active_players):
    diff_matrix = diff_matrix[sample_bill_indexes]
    frenemy_matrix = np.sum(diff_matrix, axis=0)

    friend_matrix = []
    for i, row in enumerate(frenemy_matrix):
        if i not in active_players:
            friend_matrix.append(None)
        else:
            friends = set([i for i, count in enumerate(row) if count > 0 and i in active_players])
            friend_matrix.append(friends)
    return friend_matrix


# top cover needs to be re-implemented to avoid having to expand the full preference profile
def top_cover(friend_matrix, pref_to_cc_method=smallest_cc_from_pref):
    stable_partition = set()
    pref = to_choice_sets(friend_matrix)
    while pref.keys():
        cc = pref_to_cc_method(pref)
        stable_partition.add(cc)
        friend_matrix = update_friend_matrix(friend_matrix, cc)
        pref = to_choice_sets(friend_matrix)
    return stable_partition


def to_choice_sets(friend_matrix):
    choice_sets = {}
    for i, friends in enumerate(friend_matrix):
        if friends is not None:
            choice_sets[i] = [friends]
    return choice_sets


def af_better(friend_count, max_friend_count, enemy_count, max_enemy_count):
    if friend_count > max_friend_count:
        return True
    elif friend_count == max_friend_count:
        return enemy_count < max_enemy_count
    else:
        return False


def approximate_preferences(votes, B, players, diff_matrix, coalition_matrix, sample_size, sample_method):
    S_prime_indexes = sample_method(range(len(votes)), k=sample_size)
    sample_votes = list(votes[i] for i in S_prime_indexes)
    friend_matrix = find_friends_from_sample(S_prime_indexes, diff_matrix, players)
    for i in players:
        if i in B and B[i] == {i}: # already singleton, no need to check further
            continue
        max_friend_count = 0
        max_enemy_count = len(votes[0])
        max_coalition = None
        for bill_index in S_prime_indexes:
            my_vote = votes[bill_index][i]
            if my_vote not in {1, 2}:
                continue
            voted_with_me = coalition_matrix[bill_index][i]
            friends_voted_with_me = voted_with_me & friend_matrix[i]
            friend_count = len(friends_voted_with_me)
            enemy_count = len(voted_with_me) - len(friends_voted_with_me)
            if af_better(friend_count, max_friend_count, enemy_count, max_enemy_count):
                max_friend_count = len(friends_voted_with_me)
                max_coalition = voted_with_me
                max_enemy_count = enemy_count
        old_coal_len = len(B[i]) if i in B else 0
        if max_coalition == None:
            B[i] = {i}
        else:
            if i not in B: # initialization round
                B[i] = max_coalition
            else:
                B[i] &= max_coalition
        if old_coal_len != len(B[i]):
            logging.debug(f'player {i}\'s coalition size changed: {old_coal_len} -> {len(B[i])}. {B[i]}')


def precalculate_coalitions(votes):
    coalition_matrix = []
    for row_index, row in enumerate(votes):
        coalitions = [None]*len(row)
        for_coalition = set()
        against_coalition = set()
        for col_index, vote in enumerate(row):
            if vote == 1:
                for_coalition.add(col_index)
                coalitions[col_index] = for_coalition
            elif vote == 2:
                against_coalition.add(col_index)
                coalitions[col_index] = against_coalition
        coalition_matrix.append(coalitions)
    return coalition_matrix

def pac_top_cover(votes, diff_matrix, sample_size=None, sample_method=random.choices, selective_friends=False):
    if sample_size is None:
        sample_size = len(votes)

    num_players = len(votes[0])
    players = set(range(num_players))
    stable_partition = set()
    while players:
        logging.info(f'{len(players)} players left')
        # need to redo coalition precalculation for correct & efficient counting of voted_with_me
        coalition_matrix = precalculate_coalitions(votes)
        B = {}
        approximate_preferences(votes, B, players, diff_matrix, coalition_matrix, sample_size, sample_method)
        # successive restriction loop
        for round_index in range(len(players)):
            logging.info(f'round {round_index}')
            approximate_preferences(votes, B, players, diff_matrix, coalition_matrix, sample_size, sample_method)
        logging.debug(f'done approximating preferences')

        cc = largest_scc_from_pref(B)
        stable_partition.add(cc)
        logging.info(f'players to remove: {cc}')

        players = players - cc
        # remove votes of removed players, necessary for precalculate_coalitions next iteration
        for i, row in enumerate(votes):
            for j in range(num_players):
                if j in cc:
                    votes[i][j] = None

    return stable_partition


if __name__ == '__main__':
    random.seed(42)
    original_votes, _ = read_votes_and_player_data()
    sample_size = int(0.75 * len(original_votes))
    votes = copy.deepcopy(original_votes)
    diff_matrix = precalculate_frenemy_per_player_per_bill(votes, False)
    start = time.time()
    pi = pac_top_cover(votes, diff_matrix, sample_size)
    print(f'pac_top_cover took {time.time() - start}ms')
