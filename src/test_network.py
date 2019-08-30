import unittest
from network import votes_to_graph

class TestNetwork(unittest.TestCase):

    def test_votes_to_graph(self):
        votes = [
            [1, 2, 2]
        ]
        g = votes_to_graph(votes)
        self.assertEqual(g.num_vertices(), 3)
        self.assertEqual(g.num_edges(), 1)
        self.assertEqual(g.get_edges()[0].tolist(), [1, 2])

        votes.append([1, 1, 2])
        g = votes_to_graph(votes)
        self.assertEqual(g.num_vertices(), 3)
        self.assertEqual(g.num_edges(), 2)
        edge_list = g.get_edges().tolist()
        self.assertTrue([0, 1] in edge_list)
        self.assertTrue([1, 2] in edge_list)

        votes.append([1, 1, 2])
        g = votes_to_graph(votes)
        self.assertEqual(g.num_edges(), 2)
        for e in g.edges():
            if tuple(e) == (0, 1):
                self.assertEqual(g.ep.weight[e], 2)
            elif tuple(e) == (1, 2):
                self.assertEqual(g.ep.weight[e], 1)
            else:
                print(e)
                self.assertFalse(True)


if __name__ == '__main__':
    unittest.main()

