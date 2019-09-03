from sklearn.cluster import KMeans
import numpy as np
import pandas as pd


def votes_to_np_array():
    df = pd.read_csv('data/votes_names_cleaned.csv')
    df = df.transpose()
    df.fillna(4, inplace=True) # treat missing value as "did not attend"
    df.replace(2, -1, inplace=True) # make "against" far from "for"
    df.replace([3, 4], 0, inplace=True) # treat all votes that are not "for" or "against" as neutral
    votes = np.delete(df.values, 0, axis=0)
    assert votes.shape == (147, 7489)
    return votes


def cluster_labels_to_sets(labels):
    clusters = {}
    for i, group_label in enumerate(labels):
        if group_label not in clusters:
            clusters[group_label] = set()
        clusters[group_label].add(i)
    return set(frozenset(v) for v in clusters.values())


def get_clustering_partition(k):
    X = votes_to_np_array()
    kmeans = KMeans(n_clusters=k, random_state=42).fit(X)
    return cluster_labels_to_sets(kmeans.labels_), kmeans.inertia_


if __name__ == '__main__':
    get_clustering_partition(10)
