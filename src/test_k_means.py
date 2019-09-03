import unittest
import matplotlib.pyplot as plt
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
            for k in range(2, 147):
                pi,_ = get_clustering_partition(k)
                f.write(str(pi) + '\n')
                if k % 10 == 0:
                    print(f'done cluster size: {k}')

    def test_knesset_auto_k(self):
        # scores = []
        # for k in range(2, 50):
        #     pi, score = get_clustering_partition(k)
        #     scores.append(score)
        #     if k % 10 == 0:
        #         print(f'done cluster size: {k}')
        #
        # plt.plot(range(2, 50), scores, marker='o')
        # plt.xlabel('Number of clusters')
        # plt.ylabel('Distortion')
        # plt.show()
        # # pick k = 10 because elbow
        filename = f'data/partitions_k_auto_means_1_run.txt'
        with open(filename, 'w') as f:
            pi, _ = get_clustering_partition(10)
            f.write(str(pi) + '\n')


if __name__ == '__main__':
    unittest.main()
