from collections import defaultdict, Counter
from graph_tool.all import *
from knesset_test import read_votes_and_player_data
import matplotlib.pyplot as plt
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def stochastic_block_model(g, distribution, B=None, mcmc_sweep=True):
    state_args = dict(recs=[g.ep.weight], rec_types=[distribution])
    if B:
        state = graph_tool.inference.minimize_blockmodel_dl(g, B_max=B, B_min=B, state_args=state_args)
    else:
        state = graph_tool.inference.minimize_blockmodel_dl(g, state_args=state_args)

    # slow, takes 1-5 minutes
    if mcmc_sweep:
        logging.info(f'distribution {distribution} before mcmc sweep entropy: {state.entropy()}')
        graph_tool.inference.mcmc_equilibrate(state, wait=1000, nbreaks=2, mcmc_args=dict(niter=10))
        logging.info(f'after mcmc sweep entropy: {state.entropy()}')

    blocks = state.get_blocks()
    block_map = defaultdict(list)
    for player, b in enumerate(blocks):
        block_map[b].append(player)
    pi = set()
    for coalition in block_map.values():
        pi.add(frozenset(coalition))
    return pi


def votes_to_graph(votes, allow_neg_edge=False):
    num_players = len(votes[0])
    together_counter = Counter()
    for i, bill in enumerate(votes):
        groups = defaultdict(list)
        for j, vote in enumerate(bill):
            groups[vote].append(j)
        for vote, players in groups.items():
            if vote not in {1, 2}:
                continue
            for x in range(len(players) - 1):
                for y in range(x+1, len(players)):
                    key = frozenset([players[x], players[y]])
                    together_counter[key] += 1
                    assert together_counter[key] <= len(votes), str(key) + ': ' + str(together_counter)
        if allow_neg_edge:
            for for_player in groups[1]:
                for against_player in groups[2]:
                    key = frozenset([for_player, against_player])
                    together_counter[key] -= 1

    # # for visually aiding distribution selection
    # plot_edge_weight_pmf(together_counter)

    edges = []
    for frozen_vertex_pair, weight in together_counter.items():
        vertex_pair = set(frozen_vertex_pair)
        edges.append([vertex_pair.pop(), vertex_pair.pop(), weight])

    g = Graph(directed=False)
    g.add_vertex(num_players)
    edge_weights = g.new_edge_property("int")
    g.edge_properties["weight"] = edge_weights
    g.add_edge_list(edges, eprops=[edge_weights])
    return g


def plot_edge_weight_pmf(together_counter):
    counts = list(together_counter.values())
    heights,bins = np.histogram(counts, bins=30)
    heights = heights/sum(heights)
    plt.bar(bins[:-1],heights,width=(max(bins) - min(bins))/len(bins), color="blue", alpha=0.5)
    plt.show()


if __name__ == '__main__':
    logging.info('Start reading votes data')
    votes, _ = read_votes_and_player_data()
    logging.info('Done reading votes data. Start constructing graph')
    g = votes_to_graph(votes)
    logging.info('Done constructing graph. Start building block model')
    pi = stochastic_block_model(g, "real-normal")
    print(pi)
    logging.info('All done')
