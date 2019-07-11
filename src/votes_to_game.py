
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
def value_function(i, votes, winning_vote):
    if votes[i] != winning_vote:
        return 0
    coalition = [j for j in votes if j == winning_vote]
    return 1 + 1/len(coalition)

def get_coalition(i, votes, winning_vote):
    if votes[i] != winning_vote:
        return {i}
    return set([index for index, j in enumerate(votes) if j == votes[i]])
