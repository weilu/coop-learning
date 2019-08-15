from graph_tool.all import *
from game_generator import freeze


def top_cover(pref, allow_pref_substraction=False):
    """Top covering algorithm as described in Handbook of Computational Social Choice, p371

    Parameters
    ----------
    pref : dict of player to a list of sets
        Describes every players preferences of choice sets
        e.g.
        {
           1: [{1, 2}, {1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 3}, {1, 3, 4}, {1, 4}, {1}],
           2: [{2, 3}, {2, 3, 4}, {1, 2, 3}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 2}, {2}],
           3: [{1, 3}, {1, 2, 3}, {1, 3, 4}, {1, 2, 3, 4}, {2, 3}, {2, 3, 4}, {3, 4}, {3}],
           4: [{3, 4}, {2, 3, 4}, {1, 3, 4}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 4}, {4}]
         }

    Returns
    -------
    list
        a list of sets representing the resulting stable partition
    """
    pref = freeze(pref) # prevent choice sets in pref from being modified
    stable_partition = set()
    while len(pref) > 0:
        graph, vlabel_to_index = build_graph(pref)
        smallest_cc = find_smallest_cc(graph)
        # smallest_cc = find_largest_scc(graph)
        # print('samllest_cc:', smallest_cc)
        stable_partition.add(smallest_cc)
        pref = update_preferences(pref, smallest_cc, allow_pref_substraction)
    return stable_partition

def find_largest_scc(graph):
    cc = graph_tool.topology.label_largest_component(graph)
    return frozenset([graph.vp.label[i] for i, v in enumerate(cc.a) if v == 1])

def find_smallest_cc(graph):
    smallest_cc = None
    smallest_cc_size = graph.num_vertices() + 1
    for v in graph.vertices():
        cc = graph_tool.topology.label_out_component(graph, v)
        cc_size = sum(cc.a)
        if cc_size < smallest_cc_size:
            smallest_cc_size = cc_size
            smallest_cc = cc
    return frozenset([graph.vp.label[i] for i, v in enumerate(smallest_cc.a) if v == 1])


def update_preferences(pref, smallest_cc, allow_substraction):
    new_pref = {}
    for k, v in pref.items():
        if k in smallest_cc:
            continue
        choice_set = []
        for n in v:
            new_n = frozenset(n - smallest_cc)
            if allow_substraction:
                choice_set.append(new_n)
            else:
                if new_n == n:
                    choice_set.append(n)
        new_pref[k] = choice_set
    # print('new_pref:', new_pref)
    return new_pref


def build_graph(pref):
    g = Graph()
    if len(pref) > 1:
        vlist = list(g.add_vertex(len(pref)))
    elif len(pref) == 1:
        vlist = [g.add_vertex()]
    else:
        return g, {}

    # create vertex label-to-index, and index-to-label map
    vlabel_to_index = {}
    vlabels = g.new_vertex_property("int")
    for i, player in enumerate(pref):
        vlabels[vlist[i]] = player
        vlabel_to_index[player] = i
    g.vertex_properties['label'] = vlabels

    for k, v in pref.items():
        if len(v) < 1:
            continue
        if type(v) is not list:
            v = [v]
        top_ch = v[0]
        for agent in top_ch:
            if agent == k: # ignore self
                continue
            g.add_edge(vlist[vlabel_to_index[k]], vlist[vlabel_to_index[agent]])

    # # TODO: produce debug graphs for every iteration
    # # visualize sample graph
    # pos = arf_layout(g, max_iter=0)
    # graph_draw(g, pos=pos, vertex_text=vlabels, output="sample.png")

    return g, vlabel_to_index


if __name__ == '__main__':
    # TODO: command line interface support
    pass
