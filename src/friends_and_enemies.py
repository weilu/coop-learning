from graph_tool.all import *

def stable_friends(friend_matrix):
    stable_partition = set()
    graph = build_graph(friend_matrix)
    vertex_indexes = graph.vertex_index.copy()
    while(list(graph.vertices())):
        largest_cc = find_largest_cc(graph)
        largest_cc_indexes = frozenset(vertex_indexes[v] for v in largest_cc)
        stable_partition.add(largest_cc_indexes)
        friend_matrix = update_friend_matrix(friend_matrix, largest_cc_indexes)
        graph.remove_vertex(largest_cc)

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


def find_largest_cc(graph):
    cc_graph = graph_tool.topology.extract_largest_component(graph)
    return list(cc_graph.vertices())


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

