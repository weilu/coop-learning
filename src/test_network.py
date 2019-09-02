import unittest
import random
import os.path as path
from network import votes_to_graph, stochastic_block_model
from votes_to_game import read_votes_and_player_data
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)

distribution_to_neg_edge_weight_support = {
    'real-normal': True,
    'real-exponential': False,
    'discrete-binomial': False,
    'discrete-geometric': False,
}

class TestNetwork(unittest.TestCase):

    def test_votes_to_graph(self):
        votes = [
            [1, 2, 2, 1]
        ]
        g = votes_to_graph(votes)
        self.assertEqual(g.num_vertices(), 4)
        self.assertEqual(g.num_edges(), 2)
        edge_list = g.get_edges().tolist()
        self.assertTrue([0, 3] in edge_list)
        self.assertTrue([1, 2] in edge_list)

        votes.append([1, 1, 2, 1])
        g = votes_to_graph(votes)
        self.assertEqual(g.num_vertices(), 4)
        self.assertEqual(g.num_edges(), 4)
        edge_list = g.get_edges().tolist()
        self.assertTrue([0, 1] in edge_list)
        self.assertTrue([0, 3] in edge_list)
        self.assertTrue([1, 2] in edge_list)
        self.assertTrue([1, 3] in edge_list)

        votes.append([1, 1, 2, 1])
        g = votes_to_graph(votes)
        self.assertEqual(g.num_edges(), 4)
        for e in g.edges():
            if tuple(e) == (0, 3):
                self.assertEqual(g.ep.weight[e], 3)
            elif tuple(e) == (0, 1) or tuple(e) == (1, 3):
                self.assertEqual(g.ep.weight[e], 2)
            elif tuple(e) == (1, 2):
                self.assertEqual(g.ep.weight[e], 1)
            else:
                print(e)
                self.assertFalse(True)


    def test_knesset(self):
        random.seed(42)
        for distribution, allow_neg_edge in distribution_to_neg_edge_weight_support.items():
            g = self.get_graph_from_votes(allow_neg_edge)
            for mcmc_sweep in [True, False]:
                filename = f'data/partitions_network_block_model_auto_B_{distribution}_mcmc_sweep_{mcmc_sweep}_1_run.txt'
                if path.exists(filename):
                    logging.info(f'skipping {distribution} run because {filename} already exists')
                    continue
                with open(filename, 'w') as f:
                    pi = stochastic_block_model(g, distribution, mcmc_sweep=mcmc_sweep)
                    f.write(str(pi) + '\n')


    def test_knesset_limit_num_coalitions(self):
        random.seed(42)
        for distribution, allow_neg_edge in distribution_to_neg_edge_weight_support.items():
            g = self.get_graph_from_votes(allow_neg_edge)
            filename = f'data/partitions_network_block_model_limit_B_{distribution}.txt'
            if path.exists(filename):
                logging.info(f'skipping {distribution} run because {filename} already exists')
                continue
            with open(filename, 'w') as f:
                for k in range(2, 30):
                    # disable mcmc_sweep because it'd take too long
                    pi = stochastic_block_model(g, distribution, B=k, mcmc_sweep=False)
                    f.write(str(pi) + '\n')
                    if k % 10 == 0:
                        logging.info(f'done {distribution} cluster size: {k}')


    def get_graph_from_votes(self, allow_neg_edge):
        if not hasattr(self, 'votes'):
            logging.info('Start reading votes data')
            self.votes, _ = read_votes_and_player_data()
            logging.info('Done reading votes data')
        if allow_neg_edge:
            if not hasattr(self, 'neg_edge_graph'):
                logging.info('Start constructing neg_edge_graph')
                self.neg_edge_graph = votes_to_graph(self.votes, allow_neg_edge=True)
                logging.info('Done constructing neg_edge_graph')
            return self.neg_edge_graph
        else:
            if not hasattr(self, 'graph'):
                logging.info('Start constructing graph')
                self.graph = votes_to_graph(self.votes, allow_neg_edge=False)
                logging.info('Done constructing graph')
            return self.graph


if __name__ == '__main__':
    unittest.main()

