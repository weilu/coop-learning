import csv
import glob
import re
import json
import sys
from collections import defaultdict
from partition_ids_to_names import to_partition_index_strs
from vi import variation_of_information, normalized_variation_of_information, normalized_information_distance

metric_to_fn = {
    'vi': variation_of_information,
    'nvi': normalized_variation_of_information,
    'nid': normalized_information_distance
}

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

    min_nid_part = defaultdict(dict)
    min_vi_part = defaultdict(dict)
    filename_to_partitions = {}
    for filename in files:
        partitions = []
        with open(filename) as f:
            for line in f:
                partitions.append(partition_str_to_list(line))
        if 'partitions_k_means' in filename or 'partitions_network_block_model' in filename:
            key_prefix = re.search('partitions_(.*)\.txt', filename).group(1)
            for i, p in enumerate(partitions):
                with_stats = build_partition_with_stats(p, party_partition)
                if with_stats['stats']['nid'] < min_nid_part[key_prefix].get('nid', sys.maxsize):
                    min_nid_part[key_prefix]['nid'] = with_stats['stats']['nid']
                    min_nid_part[key_prefix]['partition'] = with_stats
                if with_stats['stats']['vi'] < min_vi_part[key_prefix].get('vi', sys.maxsize):
                    min_vi_part[key_prefix]['vi'] = with_stats['stats']['vi']
                    min_vi_part[key_prefix]['partition'] = with_stats
                max_num_cluster = max(i+2, len(p))
                key = f'{key_prefix}_{max_num_cluster}_clusters'
                filename_to_partitions[key] = [with_stats]
        else:
            key = re.search('partitions_(.*)_\d+_run', filename).group(1)
            with_stats = [build_partition_with_stats(p, party_partition) for p in partitions]
            filename_to_partitions[key] = with_stats

    for k, v in min_nid_part.items():
        v['partition']['stats']['is_min_nid'] = True
    for k, v in min_vi_part.items():
        v['partition']['stats']['is_min_vi'] = True

    return filename_to_partitions


def select_representatives(grouped_partitions, metric):
    metric_fn = metric_to_fn[metric]
    reps = {}
    for key, partitions in grouped_partitions.items():
        if len(partitions) < 2:
            if f'is_min_{metric}' in partitions[0]['stats'].keys():
                print(key, partitions[0]['stats'][metric])
                reps[key] = partitions
        else:
            # pick the partition that minimizes the sum of nids to the rest of the group
            min_nid_sum = len(partitions)
            min_nid_part = partitions[0]['data']
            for i, me in enumerate(partitions):
                nid_sum = 0
                for j, other in enumerate(partitions):
                    if i == j:
                        continue
                    nid_sum += metric_fn(me['data'], other['data'])
                if nid_sum < min_nid_sum:
                    min_nid_sum = nid_sum
                    min_nid_part = me
            reps[key] = [min_nid_part]
    return reps


if __name__ == '__main__':
    grouped_partitions = gather_experiment_partitions()
    with open('../docs/partitions.json', 'w') as f:
        json.dump(grouped_partitions, f)

    representatives = select_representatives(grouped_partitions, 'nid')
    with open('../docs/partition_reps_nid.json', 'w') as f:
        json.dump(representatives, f)

    representatives = select_representatives(grouped_partitions, 'vi')
    with open('../docs/partition_reps_vi.json', 'w') as f:
        json.dump(representatives, f)
