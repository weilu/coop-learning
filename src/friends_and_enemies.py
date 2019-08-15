from graph_tool.all import *
from top_covering import smallest_cc_from_pref

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


# top cover needs to be re-implemented to avoid having to expand the full preference profile
def top_cover(friend_matrix):
    stable_partition = set()
    while friend_matrix_has_item(friend_matrix):
        pref = to_choice_sets(friend_matrix)
        smallest_cc = smallest_cc_from_pref(pref)
        stable_partition.add(smallest_cc)
        friend_matrix = update_friend_matrix(friend_matrix, smallest_cc)
    return stable_partition


def friend_matrix_has_item(friend_matrix):
    for friends in friend_matrix:
        if friends is not None:
            return True
    return False


def to_choice_sets(friend_matrix):
    choice_sets = {}
    for i, friends in enumerate(friend_matrix):
        if friends is not None:
            choice_sets[i] = [friends]
    return choice_sets
