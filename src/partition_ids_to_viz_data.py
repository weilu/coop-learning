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


# pick the partition that minimizes the sum of nids to the rest of the group
def select_representatives(grouped_partitions):
    reps = {}
    for key, partitions in grouped_partitions.items():
        if len(partitions) < 2:
            continue
        min_nid_sum = len(partitions)
        min_nid_part = partitions[0]['data']
        for i, me in enumerate(partitions):
            nid_sum = 0
            for j, other in enumerate(partitions):
                if i == j:
                    continue
                nid_sum += normalized_information_distance(me['data'], other['data'])
            if nid_sum < min_nid_sum:
                min_nid_sum = nid_sum
                min_nid_part = me
        reps[key] = [min_nid_part]
    print(reps)
    return reps


if __name__ == '__main__':
    grouped_partitions = gather_experiment_partitions()
    with open('../docs/partitions.json', 'w') as f:
        json.dump(grouped_partitions, f)

    representatives = select_representatives(grouped_partitions)
    with open('../docs/partition_reps.json', 'w') as f:
        json.dump(representatives, f)
