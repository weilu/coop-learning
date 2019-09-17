from collections import defaultdict, Counter
from itertools import combinations
import random
import logging
from votes_to_game import read_votes_and_player_data
from top_covering import largest_scc_from_pref


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def votes_to_pref_tables(votes):
    likes = defaultdict(list)
    dislikes = defaultdict(list)
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
            dislike = frozenset(against_group + [i])
            if likes[i][-1] == dislike: # avoid case where I both like and dislike to be by myself
                dislike = None
            dislikes[i].append(dislike)
        for i in against_group:
            likes[i].append(frozenset(against_group))
            dislike = frozenset(for_group + [i])
            if likes[i][-1] == dislike:
                dislike = None
            dislikes[i].append(dislike)
        for i in others_group:
            likes[i].append(None)
            dislikes[i].append(None)
    return likes, dislikes


def simplify_pref_tables(likes, dislikes):
    sl = {}
    sd = {}
    for i in likes.keys():
        liked_groups = list(c for c in likes[i] if c != None)
        disliked_groups = list(c for c in dislikes[i] if c != None)
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
        logging.info(f'{len(remaining_players)} players remaining')
        sorted_potential = sorted(potentially_stable_likes, key=len, reverse=True)
        stable_coalition = sorted_potential[0]
        stable_partition.add(stable_coalition)
        remaining_players = remaining_players - stable_coalition

        updated_potentially_stable_likes = set()
        for p in potentially_stable_likes:
            if len(stable_coalition & p) == 0:
                updated_potentially_stable_likes.add(p)
        potentially_stable_likes = updated_potentially_stable_likes

    logging.info(f'exhausted potentially_stable_likes')
    while remaining_players:
        logging.info(f'{len(remaining_players)} players remaining')
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


def approximate_preferences(players, votes, B, likes, dislikes, sample_size):
    S_prime_indexes = random.choices(range(len(votes)), k=sample_size)
    sample_votes = list(votes[i] for i in S_prime_indexes)
    filtered_likes = {}
    filtered_dislikes = {}
    for i in players:
        filtered_likes[i] = list(likes[i][j] for j in S_prime_indexes)
        filtered_dislikes[i] = list(dislikes[i][j] for j in S_prime_indexes)
    logging.info('done filtering pref tables')
    # TODO: do we really need dislikes at all?
    filtered_likes, _ = simplify_pref_tables(filtered_likes, filtered_dislikes)
    logging.info('done simplifying pref tables')
    for i in players:
        if i in B and B[i] == {i}: # already singleton, no need to check further
            continue
        if not filtered_likes[i]:
            continue
        old_coal_len = len(B[i]) if i in B else 0
        max_coalition = filtered_likes[i][0]
        if i not in B: # initialization round
            B[i] = max_coalition
        else:
            B[i] &= max_coalition
        if old_coal_len != len(B[i]):
            logging.info(f'player {i}\'s coalition size changed: {old_coal_len} -> {len(B[i])}')


def find_pac_core(votes, sample_size):
    players = set(range(len(votes[0])))
    stable_partition = set()

    while players:
        logging.info(f'{len(players)} players left')
        B = {}
        likes, dislikes = votes_to_pref_tables(votes)
        logging.info('done constructing pref tables')
        approximate_preferences(players, votes, B, likes, dislikes, sample_size)
        for round_index in range(len(players)):
            logging.info(f'round {round_index}')
            approximate_preferences(players, votes, B, likes, dislikes, sample_size)
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


# for partial preference case – consider any omitted coalition acceptable
def find_implicit_stable_coalition(all_likes, all_dislikes, remaining_players):
    for i in range(len(remaining_players)):
        k = len(remaining_players) - i # num_players, ... , 2, 1
        for coal in combinations(remaining_players, k):
            coal = frozenset(coal)
            if coal not in all_likes and coal not in all_dislikes:
                return coal

if __name__ == '__main__':
    votes, _ = read_votes_and_player_data()
    logging.info('done reading votes data')
    likes, dislikes = votes_to_pref_tables(votes)
    logging.info('done constructing pref tables')
    likes, dislikes = simplify_pref_tables(likes, dislikes)
    logging.info('done simplifying pref tables')
    pi = find_core(likes, dislikes)
    print(pi)

