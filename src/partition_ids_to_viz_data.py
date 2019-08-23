import glob
import re
import json
import sys
from partition_ids_to_names import to_partition_index_strs


def partition_str_to_list(partition_str):
    partition = []
    for coalition_str in to_partition_index_strs(partition_str):
        coalition = coalition_str.split(', ')
        partition.append([int(id_str) for id_str in coalition])
    return partition


def gather_experiment_partitions():
    files = glob.glob('data/partitions_*.txt')
    print(files)

    filename_to_partitions = {}
    for filename in files:
        partitions = []
        with open(filename) as f:
            for line in f:
                partitions.append(partition_str_to_list(line))
        key = re.search('partitions_(.*)_\d', filename).group(1)
        filename_to_partitions[key] = partitions
    return filename_to_partitions


if __name__ == '__main__':

    with open('../docs/partitions.json', 'w') as f:
        grouped_partitions = gather_experiment_partitions()
        json.dump(grouped_partitions, f)
