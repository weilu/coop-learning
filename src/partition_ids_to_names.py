import csv
import sys


def partition_str_to_list(partition_str):
    partition_index_strs = ('}), ' + partition_str[1:-1] + ', frozenset({').split('}), frozenset({')[1:-1]
    return list(coalition.split(', ') for coalition in partition_index_strs)

if __name__ == '__main__':
    partition_str = sys.argv[1]

    member_map = {}
    with open('data/members.csv') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            party_initials = ''.join(filter(str.isupper, row['party name']))
            member_map[row['index']] = party_initials + ' - ' + row['google translated name']


    pi = partition_str_to_list(partition_str)
    pi_names = []
    for coal in pi:
        coal_names = []
        for index in coal:
            coal_names.append(member_map[index])
        pi_names.append(sorted(coal_names))

    sorted_pi_names = sorted(pi_names, key=len, reverse=True)
    print(sorted_pi_names)
    print('\nOne coalition per line:')
    for coal in sorted_pi_names:
        print(coal)

