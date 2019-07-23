from operator import itemgetter

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
    return set([index for index, j in enumerate(votes) if j == votes[i]])

def value_matrix_to_preferences(value_matrix, coalition_matrix):
    game = {}
    for col in range(len(value_matrix[0])):
        values = [row[col] for row in value_matrix]
        coalitions = [row[col] for row in coalition_matrix]
        zipped = zip(values, coalitions)
        sorted_zipped = sorted(zipped, key=itemgetter(0), reverse=True)
        game[col] = [pair[1] for pair in sorted_zipped]
    return game

