from collections import defaultdict, Counter
from itertools import combinations
import random
import logging
from votes_to_game import read_votes_and_player_data
from top_covering import largest_scc_from_pref


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def votes_to_pref_table(votes):
    likes = defaultdict(list)
    for row in votes:
        for_group = []
        against_group = []
        others_group = [] # keep the likes same shape as votes
        for i, vote in enumerate(row):
            if vote == 1:
                for_group.append(i)
            elif vote == 2:
                against_group.append(i)
            else:
                others_group.append(i)
        for i in for_group:
            likes[i].append(frozenset(for_group))
        for i in against_group:
            likes[i].append(frozenset(against_group))
        for i in others_group:
            likes[i].append(None)
    return likes


def find_core(likes):
    stable_partition = set()
    remaining_players = set(likes.keys())
    while remaining_players:
        logging.info(f'{len(remaining_players)} players remaining')
        filtered_likes = {}
        for i in remaining_players:
            filtered_likes[i] = set(coal for coal in likes[i] if coal is not None)
        # coalition = find_largest_liked_coalition(filtered_likes)
        # coalition = find_a_random_liked_coalition(filtered_likes)
        coalition = find_median_sized_liked_coalition(filtered_likes)
        if coalition is not None:
            stable_partition.add(coalition)
            remaining_players = remaining_players - coalition

            # remove coalitions with removed players
            for i, row in likes.items():
                if i in coalition:
                    continue
                for j, pref_coal in enumerate(row):
                    if pref_coal is not None and (pref_coal & coalition):
                        likes[i][j] = None
        else:
            logging.info(f'exhausted all_likes')
            for i in remaining_players:
                p = frozenset([i])
                stable_partition.add(p)
            break

    return stable_partition


def find_pac_core(votes, sample_size, sample_method=random.choices):
    players = set(range(len(votes[0])))
    prefs = votes_to_pref_table(votes)
    S_prime_indexes = sample_method(range(len(votes)), k=sample_size)
    sampled_likes = {}
    for i in players:
        sampled_likes[i] = list(prefs[i][j] for j in S_prime_indexes)
    return find_core(sampled_likes)


def find_a_random_liked_coalition(prefs):
    all_likes = set()
    for liked_groups in prefs.values():
        all_likes |= liked_groups

    # all singletons left: handle at caller
    if len(all_likes) == 0:
        return None

    return random.sample(all_likes, k=1)[0]


def find_median_sized_liked_coalition(prefs):
    all_likes = set()
    for liked_groups in prefs.values():
        all_likes |= liked_groups

    # all singletons left: handle at caller
    if len(all_likes) == 0:
        return None

    sorted_potential = sorted(all_likes, key=len, reverse=True)
    median_index = int(len(all_likes)/2)
    return sorted_potential[median_index]


def find_largest_liked_coalition(prefs):
    all_likes = set()
    for liked_groups in prefs.values():
        all_likes |= liked_groups

    # all singletons left: handle at caller
    if len(all_likes) == 0:
        return None

    sorted_potential = sorted(all_likes, key=len, reverse=True)
    for coalition in sorted_potential:
        good_for_all = True
        for player in coalition:
            if coalition not in prefs[player]:
                good_for_all = False
                break
        if good_for_all:
            return coalition
