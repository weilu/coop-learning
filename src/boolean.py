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
    all_likes = set()
    for liked_groups in likes.values():
        for group in liked_groups:
            if group is not None:
                all_likes.add(group)

    remaining_players = set(likes.keys())
    while all_likes:
        logging.info(f'{len(remaining_players)} players remaining')
        sorted_potential = sorted(all_likes, key=len, reverse=True)
        stable_coalition = sorted_potential[0]
        stable_partition.add(stable_coalition)
        remaining_players = remaining_players - stable_coalition

        # remove any coalition containing any removed player
        updated_potentially_stable_likes = set()
        for p in all_likes:
            if len(stable_coalition & p) == 0:
                updated_potentially_stable_likes.add(p)
        all_likes = updated_potentially_stable_likes

    logging.info(f'exhausted all_likes')
    # all singleton coalitions
    for i in remaining_players:
        p = frozenset([i])
        stable_partition.add(p)
        remaining_players = remaining_players - p

    return stable_partition


def approximate_preferences(players, votes, B, likes, sample_size,
        sample_method=random.choices):
    S_prime_indexes = sample_method(range(len(votes)), k=sample_size)
    filtered_likes = {}
    for i in players:
        # filter out None values
        filtered_likes[i] = list(likes[i][j] for j in S_prime_indexes if likes[i][j] is not None)
    for i in players:
        if i in B and B[i] == {i}: # already singleton, no need to check further
            continue
        if not filtered_likes[i]:
            continue
        old_coal_len = len(B[i]) if i in B else 0
        sorted_likes = sorted(filtered_likes[i], key=len, reverse=True)
        max_coalition = sorted_likes[0]
        if i not in B: # initialization round
            B[i] = max_coalition
        else:
            B[i] &= max_coalition
        if old_coal_len != len(B[i]):
            logging.info(f'player {i}\'s coalition size changed: {old_coal_len} -> {len(B[i])}')


def find_pac_core(votes, sample_size, sample_method=random.choices):
    players = set(range(len(votes[0])))
    stable_partition = set()
    prefs = votes_to_pref_table(votes)

    while players:
        logging.info(f'{len(players)} players left')
        B = {}
        logging.info('done constructing pref tables')
        approximate_preferences(players, votes, B, prefs, sample_size, sample_method)
        for round_index in range(len(players)):
            approximate_preferences(players, votes, B, prefs, sample_size, sample_method)
        logging.debug(f'done approximating preferences')

        all_likes = set(B.values())
        if len(all_likes) == 0:
            logging.info(f'exhausted all_likes')
            for i in players:
                p = frozenset([i])
                stable_partition.add(p)
            break

        sorted_potential = sorted(all_likes, key=len, reverse=True)
        stable_coalition = sorted_potential[0]
        stable_partition.add(stable_coalition)
        logging.info(f'players to remove: {stable_coalition}')
        players = players - stable_coalition

        # remove coalitions with removed players
        for i, row in prefs.items():
            if i in stable_coalition:
                continue
            for j, coalition in enumerate(row):
                if coalition is not None and (coalition & stable_coalition):
                    prefs[i][j] = None

    return stable_partition
