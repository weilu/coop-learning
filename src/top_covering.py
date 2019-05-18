from graph_tool.all import *


def find_smallest_cc(graph):
    smallest_cc = None
    smallest_cc_size = graph.num_vertices()
    for v in graph.vertices():
        cc = graph_tool.topology.label_out_component(graph, v)
        cc_size = sum(cc.a)
        if cc_size < smallest_cc_size:
            smallest_cc_size = cc_size
            smallest_cc = cc
    return frozenset([graph.vp.label[i] for i, v in enumerate(smallest_cc.a) if v == 1])


def update_preferences(pref, smallest_cc):
    new_pref = {}
    for k, v in pref.items():
        if k in smallest_cc:
            continue
        choice_set_set = set() # for deduplication
        choice_set = []
        num_choice_sets = len(choice_set_set)
        for n in v:
            new_n = frozenset(n - smallest_cc)
            choice_set_set.add(new_n)
            if num_choice_sets < len(choice_set_set):
                num_choice_sets = len(choice_set_set)
                choice_set.append(new_n)
        new_pref[k] = choice_set
    return new_pref


def top_cover(pref):
    stable_partition = []
    while len(pref) > 1:
        graph, vlabel_to_index = build_graph(pref)
        smallest_cc = find_smallest_cc(graph)
        stable_partition.append(smallest_cc)
        pref = update_preferences(pref, smallest_cc)
    if len(pref) == 1:
        stable_partition.append(list(pref.values())[0][0])
    print(stable_partition)


# in: dict of player to a list of sets, each value is a player's choice set preference in descending order
# e.g. {
#        1: [{1, 2}, {1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 3}, {1, 3, 4}, {1, 4}, {1}],
#        2: [{2, 3}, {2, 3, 4}, {1, 2, 3}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 2}, {2}],
#        3: [{1, 3}, {1, 2, 3}, {1, 3, 4}, {1, 2, 3, 4}, {2, 3}, {2, 3, 4}, {3, 4}, {3}],
#        4: [{3, 4}, {2, 3, 4}, {1, 3, 4}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 4}, {4}]
#      }
def build_graph(pref):
    g = Graph()
    vlist = list(g.add_vertex(len(pref)))

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
        top_ch = v[0]
        for agent in top_ch:
            if agent == k: # ignore self
                continue
            g.add_edge(vlist[vlabel_to_index[k]], vlist[vlabel_to_index[agent]])

    # # visualize sample graph
    # graph_draw(g, vertex_text=vlabels, vertex_font_size=18,
    #            output_size=(200, 200), output="sample.png")

    return g, vlabel_to_index


def freeze(pref):
    frozen = {}
    for k, v in pref.items():
        frozen[k] = [frozenset(neighbors) for neighbors in v]
    return frozen


def generate_preferences():
    sample = {
        1: [{1, 2}, {1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 3}, {1, 3, 4}, {1, 4}, {1}],
        2: [{2, 3}, {2, 3, 4}, {1, 2, 3}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 2}, {2}],
        3: [{1, 3}, {1, 2, 3}, {1, 3, 4}, {1, 2, 3, 4}, {2, 3}, {2, 3, 4}, {3, 4}, {3}],
        4: [{3, 4}, {2, 3, 4}, {1, 3, 4}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 4}, {4}]
    }
    return freeze(sample)


if __name__ == "__main__":
    top_cover(generate_preferences())
