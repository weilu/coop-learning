from pyslet.odata2.client import Client
import pyslet.odata2.core as core
import csv
import logging
import os.path
from votes_to_game import majority

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)

BILL_RESULT_FILE = 'data/voting_results.csv'
BILL_RESULT_HEADERS = [
        'vote_id',
        'sess_item_dscr',
        'vote_item_dscr',
        'vote_date',
        'vote_time',
        'is_elctrnc_vote',
        'vote_type',
        'reason',
        'vote_stat',
        'is_accepted',
        'total_for',
        'total_against',
        'total_abstain' ]


def fetch_bill_results():
    c = Client('http://knesset.gov.il/Odata/Votes.svc/')
    with c.feeds['View_vote_rslts_hdr_Approved'].open() as res:
        filter = core.CommonExpression.from_str("knesset_num eq 20")
        res.set_filter(filter)

        with open(BILL_RESULT_FILE, 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(BILL_RESULT_HEADERS)

            for p in res.itervalues():
                csv_writer.writerow([p[key].value for key in BILL_RESULT_HEADERS])


def count_vote(vote_value, votes):
    counted_votes = [1 for i in votes if i != '' and int(i) == vote_value]
    return sum(counted_votes)


if __name__ == '__main__':
    if not os.path.exists(BILL_RESULT_FILE):
        logging.info('fetching bill voting results...')
        fetch_bill_results()

    voting_results = {}
    num_rows = 0
    with open(BILL_RESULT_FILE) as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            voting_results[row['vote_id']] = row
            num_rows += 1

    assert(len(voting_results) == num_rows)

    num_checked = 0
    num_missing = 0
    num_pass_inconsistent = 0
    num_for_inconsistent = 0
    num_against_inconsistent = 0
    num_abstained_inconsistent = 0

    with open('data/votes_names.csv') as f:
        csv_reader = csv.reader(f)
        next(csv_reader, None) # skip header

        for row in csv_reader:
            bill_id = row[0]
            votes = row[1:]
            num_for = count_vote(1, votes)
            num_against = count_vote(2, votes)
            num_abstained = count_vote(3, votes)
            passed = 1 if num_for > num_against else 0

            if bill_id not in voting_results:
                num_missing += 1
                logging.warning(f"{bill_id} cannot be checked as it's missing from the voting result csv")
                continue

            num_checked += 1
            consistent = True
            result = voting_results[bill_id]
            if passed != int(result['is_accepted']):
                consistent = False
                num_pass_inconsistent += 1
                # print(f"{bill_id}: {result['sess_item_dscr']}, {result['vote_item_dscr']}")
                logging.warning(f"{bill_id} total passed count mismatch - expected: {result['is_accepted']}, actual {passed}, "
                                f"expected for: {result['total_for']}, actual for: {num_for}, "
                                f"expected against: {result['total_against']}, actual against: {num_against}")
            if num_for != int(result['total_for']):
                consistent = False
                num_for_inconsistent += 1
                logging.warning(f"{bill_id} total for count mismatch - expected: {result['total_for']}, actual {num_for}")
            if num_against != int(result['total_against']):
                consistent = False
                num_against_inconsistent += 1
                logging.warning(f"{bill_id} total against count mismatch - expected: {result['total_against']}, actual {num_against}")
            if num_abstained != int(result['total_abstain']):
                consistent = False
                num_abstained_inconsistent += 1
                logging.warning(f"{bill_id} total abstain count mismatch - expected: {result['total_abstain']}, actual {num_abstained}")

            if consistent:
                logging.debug(f"{bill_id} values are consistent")

    print(f'Total bills checked: {num_checked},\n'
          f'Missing bill in result file: {num_missing},\n'
          f'Bill pass/reject inconsistent: {num_pass_inconsistent},\n'
          f'For count inconsistent : {num_for_inconsistent}, \n'
          f'Against count inconsistent : {num_against_inconsistent}, \n'
          f'Abstain count inconsistent : {num_abstained_inconsistent}')


