from collections import defaultdict
from votes_to_game import read_votes_and_player_data


def votes_to_pref_tables(votes):
    likes = defaultdict(list)
    dislikes = defaultdict(list)
    for row in votes:
        for_group = []
        against_group = []
        for i, vote in enumerate(row):
            if vote == 1:
                for_group.append(i)
            elif vote == 2:
                against_group.append(i)
        for i in for_group:
            likes[i].append(frozenset(for_group))
            dislike = frozenset(against_group + [i])
            if likes[i][-1] != dislike: # avoid case where I both like and dislike to be by myself
                dislikes[i].append(dislike)
        for i in against_group:
            likes[i].append(frozenset(against_group))
            dislike = frozenset(for_group + [i])
            if likes[i][-1] != dislike:
                dislikes[i].append(dislike)
    return likes, dislikes
