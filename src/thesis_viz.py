import math
import random
import numpy as np
import matplotlib.pyplot as plt
from vi import variation_of_information
from distance_measures import adjusted_mutual_information
from partition_ids_to_viz_data import read_knesset_partition_by_party


def vi_baselines():
    coalitions_by_party = read_knesset_partition_by_party()
    party_partition = set(frozenset(coalition) for coalition in coalitions_by_party.values())

    num_players = sum(len(coalition) for coalition in party_partition)
    player_list = list(range(num_players))
    all_in_one = set([frozenset(player_list)])
    singletons = set(frozenset({p}) for p in player_list)
    print(len(singletons))

    player_list_np = np.array(player_list)
    np.random.shuffle(player_list_np)
    random_splits = np.array_split(player_list_np, len(party_partition))
    random_ten = set(frozenset(coalition) for coalition in random_splits)

    vi_singletons = variation_of_information(party_partition, singletons)
    vi_all_in_one = variation_of_information(party_partition, all_in_one)
    vi_random_ten = variation_of_information(party_partition, random_ten)

    return vi_singletons, vi_all_in_one, vi_random_ten


def plot_horizontal_bars(values, x_labels, y_axis_name, max_y=None):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    bar_width = 0.6

    bar_pos = np.arange(len(x_labels))
    ax.barh(bar_pos, values, bar_width, align='center')
    ax.set_yticks(bar_pos)
    ax.set_yticklabels(x_labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(y_axis_name)
    if max_y is not None:
        ax.set_xlim([0, max_y])

    for i, v in enumerate(values):
        ax.text(v, i, str(round(v, 2)))

    plt.show()


if __name__ == '__main__':
    random.seed(42)
    vis = vi_baselines()
    x_labels = ('Singletons', 'All-in-One', 'Random 10')
    plot_horizontal_bars(vis, x_labels, 'VI', math.log(147, 2))
