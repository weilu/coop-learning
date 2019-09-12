from collections import defaultdict, Counter
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


def simplify_pref_tables(likes, dislikes):
    sl = {}
    sd = {}
    for i in likes.keys():
        liked_groups = likes[i]
        disliked_groups = dislikes[i]
        like_counts = Counter()
        dislike_counts = Counter()
        for like in liked_groups:
            like_counts[like] += 1
        for dislike in disliked_groups:
            dislike_counts[dislike] += 1
        contradictions = set(like_counts.keys()) & set(dislike_counts.keys())
        # deduplicate
        sl[i] = list(set(liked_groups) - contradictions)
        sd[i] = list(set(disliked_groups) - contradictions)
        for c in contradictions:
            # more likes = like, more or equal dislikes = dislike
            if like_counts[c] > dislike_counts[c]:
                sl[i].append(c)
            else:
                sd[i].append(c)
        # ordered by size desc
        sl[i].sort(key=len, reverse=True)
        sd[i].sort(key=len, reverse=True)

    return sl, sd
