from graph_tool.all import *

def stable_friends(friend_matrix):
    stable_partition = set()
    while(not friend_matrix_is_empty(friend_matrix)):
        graph = build_graph(friend_matrix)
        largest_cc = find_largest_cc(graph)
        # print(largest_cc)
        stable_partition.add(largest_cc)
        friend_matrix = update_friend_matrix(friend_matrix, largest_cc)

    singleton_players = get_singleton_players(friend_matrix)
    if singleton_players:
        for player in singleton_players:
            stable_partition.add(frozenset({player}))

    return stable_partition


def friend_matrix_is_empty(friend_matrix):
    for row in friend_matrix:
        if row:
            return False
    return True


def get_singleton_players(friend_matrix):
    return set(i for i, friends in enumerate(friend_matrix) if friends == set())


def build_graph(friend_matrix):
    g = Graph()
    vlist = list(g.add_vertex(len(friend_matrix)))
    for i, friends in enumerate(friend_matrix):
        if friends is None:
            continue
        g.add_edge(i, i) # add edge to self
        for friend in friends:
            g.add_edge(i, friend)
    return g


def find_largest_cc(graph):
    largest_cc = None
    largest_cc_size = 0
    for v in graph.vertices():
        cc = graph_tool.topology.label_out_component(graph, v)
        cc_size = sum(cc.a)
        if cc_size > largest_cc_size:
            largest_cc_size = cc_size
            largest_cc = cc
    return frozenset([i for i, v in enumerate(largest_cc.a) if v == 1])


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


def find_friends(votes):
    num_players = len(votes[0])
    frenemy_matrix = [[0]*num_players for _ in range(num_players)]

    for my_index in range(num_players):
        for row_index, row in enumerate(votes):
            for col_index, vote in enumerate(row):
                if col_index != my_index:
                    my_vote = row[my_index]
                    if my_vote not in [1, 2]:
                        continue
                    if vote == my_vote:
                        frenemy_matrix[my_index][col_index] += 1
                    else:
                        frenemy_matrix[my_index][col_index] -= 1

    friend_matrix = []
    for row in frenemy_matrix:
        friends = set([i for i, count in enumerate(row) if count > 0])
        friend_matrix.append(friends)
    return friend_matrix

