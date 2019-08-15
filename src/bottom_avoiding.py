from game_generator import freeze


def bottom_avoid(pref):
    pref = freeze(pref)
    stable_partition = set()
    while(set(pref.keys())):
        coalition = remove_bottom_players(pref)
        stable_partition.add(coalition)
        pref = update_preferences(pref, coalition)

    return stable_partition


def remove_bottom_players(pref):
    for i, rankings in pref.items():
        if not rankings:
            continue
        least_preferred = rankings[-1]
        if least_preferred != {i}:
            to_remove = set(least_preferred - {i}).pop()
            pref = update_preferences(pref, {to_remove})
            return remove_bottom_players(pref)
    return frozenset(pref.keys())


def update_preferences(pref, to_remove):
    new_pref = {}
    for i, rankings in pref.items():
        if i in to_remove:
            continue
        new_rankings = []
        for coal in rankings:
            if coal & to_remove:
                continue
            new_rankings.append(coal)
        new_pref[i] = new_rankings
    return new_pref

