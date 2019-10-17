import unittest
import matplotlib.pyplot as plt
from k_means import cluster_labels_to_sets, get_clustering_partition
import pickle


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
                pi, wcss, silhouette_score = get_clustering_partition(k)
                f.write(str(pi) + '\n')
                if k % 10 == 0:
                    print(f'done cluster size: {k}')

    def test_knesset_auto_k(self):
        search_range = range(2, 50)
        wcss_scores = []
        silhouette_scores = []
        for k in search_range:
            pi, wcss, silhouette_score = get_clustering_partition(k)
            wcss_scores.append(wcss)
            silhouette_scores.append(silhouette_score)
            if k % 10 == 0:
                print(f'done cluster size: {k}')

        with open('data/k-means_wcss_scores.pickle', 'wb') as fd:
            pickle.dump(wcss_scores, fd, protocol=pickle.HIGHEST_PROTOCOL)
        with open('data/k-means_silhouette_scores.pickle', 'wb') as fd:
            pickle.dump(silhouette_scores, fd, protocol=pickle.HIGHEST_PROTOCOL)

        plt.plot(search_range, wcss_scores, marker='o')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()

        plt.clf
        plt.plot(search_range, silhouette_scores, marker='o')
        plt.xlabel('Number of clusters')
        plt.ylabel('Average silhouette score')
        plt.show()

        # pick k = 10 because elbow
        filename = f'data/partitions_k_auto_means_1_run.txt'
        with open(filename, 'w') as f:
            pi, _ = get_clustering_partition(10)
            f.write(str(pi) + '\n')


if __name__ == '__main__':
    unittest.main()
