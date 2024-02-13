from f_google.big_query.client import BigQuery


def run(user: str = None) -> None:
    rows = [{'b': 'GCP'}]
    bq = BigQuery(user=user)
    bq.insert.rows_inserted(tname='noteret.tiktok2.test_insert_1', rows=rows)


run(user='RAMI')
