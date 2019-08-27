import csv
import math
import sys
import statistics
from partition_ids_to_viz_data import gather_experiment_partitions, read_knesset_partition_by_party
from vi import variation_of_information, normalized_variation_of_information, normalized_information_distance

def print_stats(label, data):
    if len(data) > 1:
        out = (f'  {label}:\n'
               f'     max: {max(data)},\n'
               f'     min: {min(data)},\n'
               f'     median: {statistics.median(data)}, \n'
               f'     mean: {statistics.mean(data)}, \n'
               f'     variance: {statistics.variance(data)}')
    else:
        out = f'  {label}: {data[0]}'
    print(out)


def print_summary_stats(key, partitions, num_coalitions, vis, nvis, nids):
    print(f'\nExperiment {key} ({len(partitions)} runs)')
    print_stats('Number of Coalitions', num_coalitions)
    print_stats('VI', vis)
    print_stats('NVI', nvis)
    print_stats('NID', nids)


if __name__ == '__main__':
    coalitions_by_party = read_knesset_partition_by_party()
    party_partition = list(coalitions_by_party.values())

    best_k_means = None
    best_k_means_nid = math.log(147, 2)
    grouped_partitions = gather_experiment_partitions()
    for key, partitions in grouped_partitions.items():
        vis = []
        nvis = []
        nids = []
        num_coalitions = []
        for part in partitions:
            num_coalitions.append(len(part['data']))
            stats = part['stats']
            vis.append(stats['vi'])
            nvis.append(stats['nvi'])
            nids.append(stats['nid'])

        if 'k_means' in key:
            if vis[0] < best_k_means_nid:
                best_k_means_nid = vis[0]
                best_k_means = (key, partitions, num_coalitions, vis, nvis, nids)
        else:
            print_summary_stats(key, partitions, num_coalitions, vis, nvis, nids)
    print_summary_stats(*best_k_means)

