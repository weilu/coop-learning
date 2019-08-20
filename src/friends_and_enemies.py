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


def find_friends(votes, active_players=None):
    num_players = len(votes[0])
    frenemy_matrix = [[0]*num_players for _ in range(num_players)]

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
                        frenemy_matrix[my_index][col_index] += 1
                    else:
                        frenemy_matrix[my_index][col_index] -= 1

    logging.info('done calculating frenemy_matrix')

    friend_matrix = []
    for i, row in enumerate(frenemy_matrix):
        if active_players and i not in active_players:
            friend_matrix.append(None)
        else:
            friends = set([i for i, count in enumerate(row) if count > 0])
            if active_players:
                friends &= active_players
            friend_matrix.append(friends)
    logging.info('done constructing friend_matrix')
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
