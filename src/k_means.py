from sklearn.cluster import KMeans
import numpy as np
import pandas as pd


def votes_to_np_array():
    df = pd.read_csv('data/votes_names_cleaned.csv', skiprows=[0])
    df = df.transpose()
    df.fillna(4, inplace=True)
    votes = df.values[:, 1:]
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
    return cluster_labels_to_sets(kmeans.labels_)


if __name__ == '__main__':
    get_clustering_partition(10)
