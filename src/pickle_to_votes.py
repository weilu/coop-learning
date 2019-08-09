import csv
import pickle

def load_pickle(pickle_file):
    with open(pickle_file, 'rb') as pf:
        return pickle.load(pf)


if __name__ == '__main__':
    #{<vote_id>: { "kmmbrs2votes": {<kmmbr_id>: <vote_result>}}
    laws = load_pickle('data/laws2.pickle')

    #{<kmmbr_id>: {kmmbr_name: <kmmbr_name>,
    #              faction_id: <faction_id>,
    #              faction_name: <faction_name> }}
    kmmbrs = load_pickle('data/kmmrs2.pickle')

    kmmbr_ids = set()
    for _, wrapper in laws.items():
        kmmbr_ids |= wrapper['kmmbrs2votes'].keys()

    sorted_kmmbr_ids = sorted(kmmbr_ids)
    sorted_kmmbr_names = [kmmbrs[i]['kmmbr_name'] for i in sorted_kmmbr_ids]

    with open('data/member_names.csv', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['index', 'name', 'party'])

        for index, name in enumerate(sorted_kmmbr_names):
            kmmbr_id = sorted_kmmbr_ids[index]
            row = [index, name, kmmbrs[kmmbr_id]['faction_name']]
            csv_writer.writerow(row)

    with open('data/votes_names.csv', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['vote_id'] + sorted_kmmbr_names)

        for vote_id, wrapper in laws.items():
            row = [None]*len(sorted_kmmbr_ids)
            for kmmbr_id, vote in wrapper['kmmbrs2votes'].items():
                index = sorted_kmmbr_ids.index(kmmbr_id)
                row[index] = vote
            # assert(None not in row)
            csv_writer.writerow([vote_id] + row)

