import unittest
from operator import itemgetter
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


    def test_knesset_auto_k(self):
        max_silhouette_score = -1
        max_silhouette_parition = None
        k_and_scores = []
        for k in range(2, 100):
            pi, score = get_clustering_partition(k)
            k_and_scores.append((k, score))
            if score > max_silhouette_score:
                max_silhouette_score = score
                max_silhouette_parition = pi
                print(f'max k updated: {k}, score: {score}')
            if k % 10 == 0:
                print(f'done cluster size: {k}')

        for pair in sorted(k_and_scores, key=itemgetter(1), reverse=True):
            print(pair)
        filename = f'data/partitions_k_means_1_run.txt'
        with open(filename, 'w') as f:
            f.write(str(max_silhouette_parition) + '\n')

if __name__ == '__main__':
    unittest.main()
