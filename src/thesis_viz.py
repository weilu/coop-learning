import math
import glob
import random
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
from vi import variation_of_information
from distance_measures import adjusted_mutual_information
from partition_ids_to_viz_data import read_knesset_partition_by_party, partition_str_to_list
from partition_stats import print_stats


def baseline_partitions():
    coalitions_by_party = read_knesset_partition_by_party()
    party_partition = set(frozenset(coalition) for coalition in coalitions_by_party.values())

    num_players = sum(len(coalition) for coalition in party_partition)
    player_list = list(range(num_players))
    all_in_one = set([frozenset(player_list)])
    singletons = set(frozenset({p}) for p in player_list)

    player_list_np = np.array(player_list)
    np.random.shuffle(player_list_np)
    random_splits = np.array_split(player_list_np, len(party_partition))
    random_ten = set(frozenset(coalition) for coalition in random_splits)

    return party_partition, singletons, all_in_one, random_ten


def vi_baselines(truth_partition, *baseline_partitions):
    return list(variation_of_information(truth_partition, p) for p in baseline_partitions)

def ami_baselines(truth_partition, *baseline_partitions):
    return list(adjusted_mutual_information(truth_partition, p) for p in baseline_partitions)

def plot_horizontal_bars(values, x_labels, y_axis_name, min_y=None, max_y=None):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    bar_width = 0.6

    bar_pos = np.arange(len(x_labels))
    ax.barh(bar_pos, values, bar_width, align='center')
    ax.set_yticks(bar_pos)
    ax.set_yticklabels(x_labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(y_axis_name)
    if min_y is not None and max_y is not None:
        ax.set_xlim([min_y, max_y])

    for i, v in enumerate(values):
        ax.text(v, i, str(round(v, 2)))

    plt.show()

def quantitative_measurement_baselines():
    party_partition, singletons, all_in_one, random_ten = baseline_partitions()
    x_labels = ('Singletons', 'All-in-One', 'Random 10')

    # vis = vi_baselines(party_partition, singletons, all_in_one, random_ten)
    # plot_horizontal_bars(vis, x_labels, 'VI', min_y=0, max_y=math.log(147, 2))

    amis = ami_baselines(party_partition, singletons, all_in_one, random_ten)
    print(amis)
    plot_horizontal_bars(amis, x_labels, 'AMI')


def calculate_pair_wise_amis(partitions):
    scores = []
    for i in range(len(partitions) - 1):
        p1 = partitions[i]
        for j in range(i+1, len(partitions)):
            p2 = partitions[j]
            scores.append(adjusted_mutual_information(p1, p2))
    return scores


def pac_variability():
    files = glob.glob('data/partitions_*_50_runs.txt')
    print(files)
    for filename in files:
        partitions = []
        with open(filename) as f:
            key = re.search('partitions_(.*)_\d+_run', filename).group(1)
            for line in f:
                pi = partition_str_to_list(line)
                partitions.append(pi)
            print(f'\nExperiment {key}')
        num_coalitions = list(len(pi) for pi in partitions)
        print_stats('Number of Coalitions', num_coalitions)
        amis = calculate_pair_wise_amis(partitions)
        print_stats('Pair-wise AMIs', amis)

if __name__ == '__main__':
    random.seed(42)
    # quantitative_measurement_baselines()
    pac_variability()

