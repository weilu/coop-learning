from friends import update_friend_matrix

def bottom_avoid(friend_matrix):
    stable_partition = set()
    pref = to_avoid_sets(friend_matrix)
    while pref.keys():
        coalition = remove_bottom_players(pref, friend_matrix)
        stable_partition.add(coalition)
        friend_matrix = update_friend_matrix(friend_matrix, coalition)
        pref = to_avoid_sets(friend_matrix)

    return stable_partition


def remove_bottom_players(pref, friend_matrix):
    for i, least_preferred in pref.items():
        if not least_preferred:
            continue
        if least_preferred != {i}:
            to_remove = set(least_preferred - {i}).pop()
            friend_matrix = update_friend_matrix(friend_matrix, {to_remove})
            pref = to_avoid_sets(friend_matrix)
            return remove_bottom_players(pref, friend_matrix)
    return frozenset(pref.keys())


def to_avoid_sets(friend_matrix):
    active_players = set()
    for i, friends in enumerate(friend_matrix):
        if friends is not None:
            active_players.add(i)

    avoid_sets = {}
    for i, friends in enumerate(friend_matrix):
        if friends is not None:
            avoid_sets[i] = active_players - friends
    return avoid_sets


