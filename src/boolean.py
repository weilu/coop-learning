from collections import defaultdict, Counter
from itertools import combinations
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


def find_core(likes, dislikes):
    stable_partition = set()
    all_likes = set()
    all_dislikes = set()
    for liked_groups in likes.values():
        all_likes |= set(liked_groups)
    for disliked_groups in dislikes.values():
        all_dislikes |= set(disliked_groups)
    potentially_stable_likes = all_likes - all_dislikes

    remaining_players = set(likes.keys())
    while potentially_stable_likes:
        sorted_potential = sorted(potentially_stable_likes, key=len, reverse=True)
        stable_coalition = sorted_potential[0]
        stable_partition.add(stable_coalition)
        remaining_players = remaining_players - stable_coalition

        updated_potentially_stable_likes = set()
        for p in potentially_stable_likes:
            if len(stable_coalition & p) == 0:
                updated_potentially_stable_likes.add(p)
        potentially_stable_likes = updated_potentially_stable_likes

    while remaining_players:
        p = find_implicit_stable_coalition(all_likes, all_dislikes, remaining_players)
        if not p: # all singleton coalitions
            for i in remaining_players:
                p = frozenset([i])
                stable_partition.add(p)
                remaining_players = remaining_players - p
            break
        stable_partition.add(p)
        remaining_players = remaining_players - p

    return stable_partition


def find_implicit_stable_coalition(all_likes, all_dislikes, remaining_players):
    for i in range(len(remaining_players)):
        k = len(remaining_players) - i # num_players, ... , 2, 1
        for coal in combinations(remaining_players, k):
            coal = frozenset(coal)
            if coal not in all_likes and coal not in all_dislikes:
                return coal

if __name__ == '__main__':
    votes, _ = read_votes_and_player_data()
    likes, dislikes = votes_to_pref_tables(votes)
    likes, dislikes = simplify_pref_tables(likes, dislikes)

