import csv
import sys
import statistics
from partition_ids_to_viz_data import gather_experiment_partitions
from vi import variation_of_information

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


def print_stats(label, data):
    out = (f'  {label}:\n'
          f'     max: {max(data)},\n'
          f'     min: {min(data)},\n'
          f'     median: {statistics.median(data)}, \n'
          f'     mean: {statistics.mean(data)}')
    if len(data) > 1:
        out += f'\n     variance: {statistics.variance(data)}'
    print(out)

if __name__ == '__main__':
    coalitions_by_party = read_knesset_partition_by_party()
    party_partition = list(coalitions_by_party.values())

    grouped_partitions = gather_experiment_partitions()
    for key, partitions in grouped_partitions.items():
        print(f'\nExperiment {key} ({len(partitions)} runs)')
        vis = []
        num_coalitions = []
        for part in partitions:
            num_coalitions.append(len(part))
            vi = variation_of_information(part, party_partition)
            vis.append(vi)
        print_stats('Number of Coalitions', num_coalitions)
        print_stats('VI', vis)

