import csv
import sys
import numpy as np
from scipy.optimize import linear_sum_assignment
from operator import itemgetter
from collections import Counter

def majority(votes):
    # 1 is for, 2 is against, others are ignored
    # tie broken in favor of against
    valid_votes = [i for i in votes if i in (1, 2)]
    if len(valid_votes) == 0:
        return 2
    binary_votes = [i - 1 for i in valid_votes]
    if sum(binary_votes) / len(binary_votes) < 0.5:
        return 1
    else:
        return 2

# how happy an individual player is
def value_function(i, votes, winning_vote, participation=False):
    if votes[i] != winning_vote:
        return 0
    coalition = [j for j in votes if j == winning_vote]
    value = 1 + 1/len(coalition)
    if participation:
        num_valid_votes = sum([1 for j in votes if j in (1, 2)])
        value += num_valid_votes/len(votes)
    return value

def get_coalition(i, votes, winning_vote):
    if votes[i] != winning_vote:
        return {i}
    return frozenset([index for index, j in enumerate(votes) if j == votes[i]])

def value_matrix_to_preferences(value_matrix, coalition_matrix):
    game = {}
    for col in range(len(value_matrix[0])):
        values = []
        coalitions = []
        for i, row in enumerate(coalition_matrix):
            value = value_matrix[i][col]
            if row[col] not in coalitions and value > 0:
                coalitions.append(row[col])
                values.append(value)
        zipped = zip(values, coalitions)
        sorted_zipped = sorted(zipped, key=itemgetter(0), reverse=True)
        game[col] = [pair[1] for pair in sorted_zipped]
    return game


def partition_edit_distance(part1, part2):
    max_num_parts = max(len(part1), len(part2))
    max_coal_size = max(max(len(col) for col in part1),
                        max(len(col) for col in part2))
    cost_matrix = np.full((max_num_parts, max_num_parts), max_coal_size)

    part1 = list(part1)
    part2 = list(part2)
    for i in range(max_num_parts):
        for j in range(max_num_parts):
            cost = max_coal_size
            if i >= len(part1) and j < len(part2):
                cost = len(part2[j])
            elif i < len(part1) and j >= len(part2):
                cost = len(part1[i])
            else: # both present
                num_common = len(part1[i] & part2[j])
                cost = len(part1[i] | part2[j]) - num_common
            cost_matrix[i, j] = cost

    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    ordered_part1 = to_ordered_partition(part1, row_ind)
    ordered_part2 = to_ordered_partition(part2, col_ind)
    # divide by 2 because each cost is accounted for twice
    return cost_matrix[row_ind, col_ind].sum(), list(zip(ordered_part1, ordered_part2))


def to_ordered_partition(partition, indexes):
    ordered_part = []
    for i in indexes:
        if i < len(partition):
            ordered_part.append(partition[i])
        else:
            ordered_part.append(frozenset())
    return ordered_part


def precalculate_valuations_and_coalitions(S):
    winning_votes = list(map(majority, S))
    value_matrix = []
    coalition_matrix = []
    for row_index, row in enumerate(S):
        winning_vote = winning_votes[row_index]
        values = []
        coalitions = []
        for col_index, vote in enumerate(row):
            values.append(value_function(col_index, row, winning_vote, participation=True))
            coalitions.append(get_coalition(col_index, row, winning_vote))
        value_matrix.append(values)
        coalition_matrix.append(coalitions)
    return value_matrix, coalition_matrix


def read_votes_and_player_data():
    with open('data/votes_names_cleaned.csv') as f:
        reader = csv.reader(f)
        player_labels = next(reader, None)
        player_labels = player_labels[1:]
        votes = [[int(i) if i != '' else '' for i in row[1:]] for row in reader]
        return votes, player_labels


def count_votes_per_player(votes):
    vote_counter = Counter()
    for row in votes:
        for player, vote in enumerate(row):
            if vote in [1, 2]:
                vote_counter[player] += 1
    return vote_counter


def filter_infrequent_voters(min_num_votes):
    votes, player_labels = read_votes_and_player_data()
    vote_counter = count_votes_per_player(votes)

    all_players = set(player for player in vote_counter.keys())
    remaining_players = set(player for player, num_votes in vote_counter.items() if num_votes > min_num_votes)
    rejects = sorted(list(all_players - remaining_players), reverse=True)
    print(rejects)

    for idx in rejects:
        del player_labels[idx]
        for row in votes:
            del row[idx]

    return votes, player_labels


if __name__ == '__main__':
    votes, player_labels = read_votes_and_player_data()
    vote_counter = count_votes_per_player(votes)
    for i in range(len(votes[0])):
        # for sankey.json
        print(f'{vote_counter[i]},')
    # for quick barchart with Tableau
    with open('data/vote_count_by_member.csv', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['name', 'num_votes'])
        for t in sorted(vote_counter, key=vote_counter.get, reverse=True):
            csv_writer.writerow([player_labels[t], vote_counter[t]])
