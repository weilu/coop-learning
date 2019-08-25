import csv
import glob
import re
import json
import sys
from partition_ids_to_names import to_partition_index_strs
from vi import variation_of_information, normalized_variation_of_information, normalized_information_distance


def read_knesset_partition_by_party():
    coalitions_by_party = {}
    with open('data/member_names.csv') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            party = row['party']
            idx = int(row['index'])
            if party not in coalitions_by_party:
                coalitions_by_party[party] = []
            coalitions_by_party[party].append(idx)
    return coalitions_by_party


def partition_str_to_list(partition_str):
    partition = []
    for coalition_str in to_partition_index_strs(partition_str):
        coalition = coalition_str.split(', ')
        partition.append([int(id_str) for id_str in coalition])
    partition = sorted(partition, key=len, reverse=True)
    return partition


def build_partition_with_stats(p, party_partition):
    vi = variation_of_information(p, party_partition)
    nvi = normalized_variation_of_information(p, party_partition)
    nid = normalized_information_distance(p, party_partition)
    stats = {'vi': vi, 'nvi': nvi, 'nid': nid}
    part_with_stats = {'data': p, 'stats': stats}
    return part_with_stats


def gather_experiment_partitions():
    files = glob.glob('data/partitions_*.txt')
    print(files)

    coalitions_by_party = read_knesset_partition_by_party()
    party_partition = list(coalitions_by_party.values())

    filename_to_partitions = {}
    for filename in files:
        partitions = []
        with open(filename) as f:
            for line in f:
                partitions.append(partition_str_to_list(line))
        if 'partitions_k_means' in filename:
            for p in partitions:
                with_stats = build_partition_with_stats(p, party_partition)
                filename_to_partitions[f'k_means_{len(p)}_clusters'] = [with_stats]
        else:
            key = re.search('partitions_(.*)_\d+_run', filename).group(1)
            with_stats = [build_partition_with_stats(p, party_partition) for p in partitions]
            filename_to_partitions[key] = with_stats
    return filename_to_partitions


if __name__ == '__main__':

    with open('../docs/partitions.json', 'w') as f:
        grouped_partitions = gather_experiment_partitions()
        json.dump(grouped_partitions, f)
