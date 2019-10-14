import csv
import glob
import re
import json
import sys
from collections import defaultdict
from partition_ids_to_names import to_partition_index_strs
from vi import variation_of_information, normalized_variation_of_information, normalized_information_distance
from distance_measures import normalized_mutual_information, adjusted_mutual_information
import warnings
warnings.filterwarnings("ignore")

metric_to_fn = {
    'vi': variation_of_information,
    'nid': normalized_information_distance,
    'nmi': normalized_mutual_information,
    'ami': adjusted_mutual_information
}

metric_to_minimize = {
    'vi': True,
    'nid': True,
    'nmi': False,
    'ami': False
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
    nmi = normalized_mutual_information(p, party_partition)
    ami = adjusted_mutual_information(p, party_partition)
    stats = {'vi': vi, 'nvi': nvi, 'nid': nid, 'nmi': nmi, 'ami': ami}
    part_with_stats = {'data': p, 'stats': stats}
    return part_with_stats


def gather_experiment_partitions():
    files = glob.glob('data/partitions_*.txt')
    print(files)

    coalitions_by_party = read_knesset_partition_by_party()
    party_partition = list(coalitions_by_party.values())

    min_nid_part = defaultdict(dict)
    min_vi_part = defaultdict(dict)
    max_nmi_part = defaultdict(dict)
    max_ami_part = defaultdict(dict)
    filename_to_partitions = {}
    for filename in files:
        partitions = []
        with open(filename) as f:
            for line in f:
                partitions.append(partition_str_to_list(line))
        print(filename)
        if 'partitions_k_means' in filename or 'partitions_network_block_model_limit_B' in filename:
            key_prefix = re.search('partitions_(.*)\.txt', filename).group(1)
            for i, p in enumerate(partitions):
                with_stats = build_partition_with_stats(p, party_partition)
                key = f'{key_prefix}_{len(p)}_clusters'
                filename_to_partitions[key] = [with_stats]
                if with_stats['stats']['nid'] < min_nid_part[key_prefix].get('nid', sys.maxsize):
                    min_nid_part[key_prefix]['nid'] = with_stats['stats']['nid']
                    min_nid_part[key_prefix]['partition'] = with_stats
                if with_stats['stats']['vi'] < min_vi_part[key_prefix].get('vi', sys.maxsize):
                    min_vi_part[key_prefix]['vi'] = with_stats['stats']['vi']
                    min_vi_part[key_prefix]['partition'] = with_stats
                if with_stats['stats']['nmi'] > max_nmi_part[key_prefix].get('nmi', -sys.maxsize):
                    max_nmi_part[key_prefix]['nmi'] = with_stats['stats']['nmi']
                    max_nmi_part[key_prefix]['partition'] = with_stats
                if with_stats['stats']['ami'] > max_ami_part[key_prefix].get('ami', -sys.maxsize):
                    max_ami_part[key_prefix]['ami'] = with_stats['stats']['ami']
                    max_ami_part[key_prefix]['partition'] = with_stats
        else:
            match = re.search('partitions_(.*)_\d+_run', filename)
            if not match:
                print(f'unrecognized file name format: {filename}')
                continue
            key = match.group(1)
            with_stats = [build_partition_with_stats(p, party_partition) for p in partitions]
            filename_to_partitions[key] = with_stats

    for k, v in min_nid_part.items():
        v['partition']['stats']['is_min_nid'] = True
    for k, v in min_vi_part.items():
        v['partition']['stats']['is_min_vi'] = True
    for k, v in max_nmi_part.items():
        v['partition']['stats']['is_max_nmi'] = True
    for k, v in max_ami_part.items():
        v['partition']['stats']['is_max_ami'] = True

    return filename_to_partitions


SINGLE_RUN_MODELS = [
    'network_block_model_auto_B_discrete-geometric_mcmc_sweep_True',
    'network_block_model_auto_B_real-normal_mcmc_sweep_True',
    'k_auto_means',
    'boolean',
    'value_function',
    'friends',
    'selective_friends',
    'enemies',
    'enemies_selective',
]

def select_representatives(grouped_partitions, metric):
    metric_fn = metric_to_fn[metric]
    reps = {}
    for key, partitions in grouped_partitions.items():
        print_stats = True
        if len(partitions) < 1:
            print(f'Ignoring {key} as no valid partition found')
            continue
        elif len(partitions) == 1:
            stats_keys = partitions[0]['stats'].keys()
            if key in SINGLE_RUN_MODELS:
                reps[key] = partitions
            else:
                print_stats = False
        else:
            if metric_to_minimize[metric]:
                # pick the partition that minimizes the sum of distance to the rest of the group
                min_nid_sum = sys.maxsize
                min_nid_part = None
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
            else:
                max_metric_sum = -sys.maxsize
                max_metric_part = None
                for i, me in enumerate(partitions):
                    metric_sum = 0
                    for j, other in enumerate(partitions):
                        if i == j:
                            continue
                        metric_sum += metric_fn(me['data'], other['data'])
                    if metric_sum > max_metric_sum:
                        max_metric_sum = metric_sum
                        max_metric_part = me
                reps[key] = [max_metric_part]

        if print_stats:
            print(metric, key, partitions[0]['stats'][metric])
    return reps


if __name__ == '__main__':
    grouped_partitions = gather_experiment_partitions()
    with open('../docs/partitions.json', 'w') as f:
        json.dump(grouped_partitions, f)

    for metric in metric_to_fn.keys():
        representatives = select_representatives(grouped_partitions, metric)
        with open(f'../docs/partition_reps_{metric}.json', 'w') as f:
            json.dump(representatives, f)
        print(f'Done {metric}\n')
