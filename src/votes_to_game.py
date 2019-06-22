
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

def value_function(i, votes):
    #TODO: clarify if this is the value to group or player
    winning_vote = majority(votes)
    if votes[i] != winning_vote:
        return 0
    coalition = [j for j in votes if j == winning_vote]
    return 1 + 1/len(coalition)

def get_coalition(i, votes):
    #TODO: clarify how to handle when i is never in a winning coalition?
    # A: {i} or B: randomly pick a losing coalition
    # option A makes more sense to me as the coalition size is smallest
    winning_vote = majority(votes)
    if votes[i] != winning_vote:
        return {i}
    return set([index for index, j in enumerate(votes) if j == votes[i]])
