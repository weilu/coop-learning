from partition_ids_to_names import partition_str_to_set
from knesset_test import calculate_partition_edit_distances_and_print_stats


def read_partitions(filename):
    partitions = []
    with open(filename) as f:
        for line in f:
            partitions.append(partition_str_to_set(line))
    return partitions


if __name__ == '__main__':
    print('All coalitions:')
    partitions = read_partitions('data/partitions_pac_friends_43_runs.txt')
    calculate_partition_edit_distances_and_print_stats(partitions)

    print('Largest two coalitions:')
    largest_two_coalitions_list = []
    for partition in partitions:
        largest_two_coalitions = set(sorted(partition, key=len, reverse=True)[0:2])
        largest_two_coalitions_list.append(largest_two_coalitions)
    calculate_partition_edit_distances_and_print_stats(largest_two_coalitions_list)
