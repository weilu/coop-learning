from sklearn import metrics


def normalized_mutual_information(partition1, partition2):
    if type(partition1[0]) in [list, set, frozenset]:
        p1 = to_label_array(partition1)
        p2 = to_label_array(partition2)
    assert len(p1) == len(p2), f'diff len: {len(p1)} vs {len(p2)}\n {partition1} -> {p1}, {partition2} -> {p2}'
    return metrics.normalized_mutual_info_score(p1, p2)


def adjusted_mutual_information(partition1, partition2):
    if type(partition1) == set or (type(partition1[0]) in [list, set, frozenset]):
        partition1 = to_label_array(partition1)
        partition2 = to_label_array(partition2)
    return metrics.adjusted_mutual_info_score(partition1, partition2, average_method='max')


def to_label_array(pi):
    labels = [None for coalition in pi for player in coalition ]
    for group_idx, coalition in enumerate(pi):
        for player_idx, player in enumerate(coalition):
            labels[player] = group_idx
    return labels
