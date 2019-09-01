import unittest
import random
import os.path as path
from network import votes_to_graph, stochastic_block_model
from knesset_test import read_votes_and_player_data
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


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
        votes, _ = read_votes_and_player_data()
        configs = [
            ('real-normal', True),
            ('real-exponential', False),
            ('discrete-binomial', False),
            ('discrete-geometric', False),
        ]
        for distribution, allow_neg_edge in configs:
            g = votes_to_graph(votes, allow_neg_edge)
            filename = f'data/partitions_network_block_model_auto_B_mcmc_sweep_{distribution}_1_run.txt'
            if path.exists(filename):
                logging.info(f'skipping {distribution} run because {filename} already exists')
                continue
            with open(filename, 'w') as f:
                pi = stochastic_block_model(g, distribution)
                f.write(str(pi) + '\n')


    def test_knesset_limit_num_coalitions(self):
        random.seed(42)
        votes, _ = read_votes_and_player_data()
        configs = [
            ('real-normal', True),
            ('real-exponential', False),
            ('discrete-binomial', False),
            ('discrete-geometric', False),
        ]
        for distribution, allow_neg_edge in configs:
            g = votes_to_graph(votes, allow_neg_edge)
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


if __name__ == '__main__':
    unittest.main()

