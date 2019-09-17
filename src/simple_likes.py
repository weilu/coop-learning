from collections import defaultdict
import logging
import random
from top_covering import largest_scc_from_pref


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def votes_to_likes_tables(votes):
    likes = defaultdict(list)
    for row in votes:
        for_group = []
        against_group = []
        others_group = [] # keep the likes and dislikes same shape as votes
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


def approximate_preferences(players, votes, B, likes, sample_size, sample_method):
    S_prime_indexes = sample_method(range(len(votes)), k=sample_size)
    sample_votes = list(votes[i] for i in S_prime_indexes)
    filtered_likes = {}
    for i in players:
        if i in B and B[i] == {i}: # already singleton, no need to check further
            continue
        max_coalition = {i}
        for j in S_prime_indexes:
            coalition = likes[i][j]
            if not coalition:
                continue
            if len(coalition) > len(max_coalition):
                max_coalition = coalition
        old_coal_len = len(B[i]) if i in B else 0
        if i not in B: # initialization round
            B[i] = max_coalition
        else:
            B[i] &= max_coalition
        if old_coal_len != len(B[i]):
            logging.info(f'player {i}\'s coalition size changed: {old_coal_len} -> {len(B[i])}')


def find_pac_core(votes, sample_size, sample_method=random.choices):
    players = set(range(len(votes[0])))
    stable_partition = set()

    while players:
        logging.info(f'{len(players)} players left')
        B = {}
        likes = votes_to_likes_tables(votes)
        logging.info('done constructing pref tables')
        approximate_preferences(players, votes, B, likes, sample_size, sample_method)
        for round_index in range(len(players)):
            logging.info(f'round {round_index}')
            approximate_preferences(players, votes, B, likes, sample_size, sample_method)
        logging.debug(f'done approximating preferences')

        largest_scc = largest_scc_from_pref(B)
        stable_partition.add(largest_scc)
        logging.info(f'players to remove: {largest_scc}')
        players = players - largest_scc

        # change removed players' votes to neutral
        for i, row in enumerate(votes):
            for j, vote in enumerate(row):
                if j in largest_scc and vote in (1, 2):
                    row[j] = None
    return stable_partition

