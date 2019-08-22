import re
import json
import sys

def partition_str_to_list(partition_str):
    partition_index_strs = ('}), ' + partition_str[1:-1] + ', frozenset({').split('}), frozenset({')[1:-1]
    partition = []
    for coalition_str in partition_index_strs:
        coalition = coalition_str.split(', ')
        partition.append([int(id_str) for id_str in coalition])
    return partition

if __name__ == '__main__':
    files = sys.argv[1:]

    filename_to_partitions = {}
    for filename in files:
        partitions = []
        with open(filename) as f:
            for line in f:
                partitions.append(partition_str_to_list(line))
        key = re.search('partitions_(.*)_\d', filename).group(1)
        filename_to_partitions[key] = partitions

    with open('../docs/partitions.json', 'w') as f:
        json.dump(filename_to_partitions, f)
