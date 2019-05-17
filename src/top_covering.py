from graph_tool.all import *


def top_cover(pref):
    graph, vlabel_to_index = build_graph(pref)
    smallest_cc = None
    smallest_cc_size = len(pref)
    for v in graph.vertices():
        cc = graph_tool.topology.label_out_component(graph, v)
        cc_size = sum(cc.a)
        if cc_size < smallest_cc_size:
            smallest_cc_size = cc_size
            smallest_cc = cc
    print(smallest_cc.a)


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


def generate_preferences():
    return {
        1: [{1, 2}, {1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 3}, {1, 3, 4}, {1, 4}, {1}],
        2: [{2, 3}, {2, 3, 4}, {1, 2, 3}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 2}, {2}],
        3: [{1, 3}, {1, 2, 3}, {1, 3, 4}, {1, 2, 3, 4}, {2, 3}, {2, 3, 4}, {3, 4}, {3}],
        4: [{3, 4}, {2, 3, 4}, {1, 3, 4}, {1, 2, 3, 4}, {2, 4}, {1, 2, 4}, {1, 4}, {4}]
    }


if __name__ == "__main__":
    top_cover(generate_preferences())
