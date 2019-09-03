import unittest
from k_means import cluster_labels_to_sets, get_clustering_partition


class TestKMeans(unittest.TestCase):

    def test_cluster_labels_to_sets(self):
        pi = cluster_labels_to_sets([1, 1, 2, 3])
        self.assertEqual(len(pi), 3)
        self.assertTrue(frozenset([0, 1]) in pi)
        self.assertTrue(frozenset([2]) in pi)
        self.assertTrue(frozenset([3]) in pi)

        pi = cluster_labels_to_sets([0, 0, 0, 1])
        self.assertEqual(len(pi), 2)
        self.assertTrue(frozenset([0, 1, 2]) in pi)
        self.assertTrue(frozenset([3]) in pi)

    def test_knesset(self):
        filename = f'data/partitions_k_means.txt'
        with open(filename, 'w') as f:
            for k in range(2, 130):
                pi = get_clustering_partition(k)
                f.write(str(pi) + '\n')
                if k % 10 == 0:
                    print(f'done cluster size: {k}')


if __name__ == '__main__':
    unittest.main()
