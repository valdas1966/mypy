from f_google.services.big_query.client import BigQuery


bq = BigQuery(user='RAMI')

print(bq.user)
print(bq.creds)

cnt = bq.select.df(query='select count(*) from noteret.tiktok.temp_2')
print(cnt)

