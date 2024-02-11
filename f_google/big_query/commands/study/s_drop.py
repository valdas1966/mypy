from f_google.big_query.client import ClientBigQuery


bq = ClientBigQuery(user='RAMI')
bq.drop.table(name='noteret.tiktok2.temp_1')
