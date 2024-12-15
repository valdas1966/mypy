from f_google.services.big_query.client import BigQuery


bq = BigQuery(user='RAMI')
bq.drop.table(tname='noteret.tiktok2.temp_1', verbose=False)
