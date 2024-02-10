from f_google.big_query.client import Client


bq = Client(user='RAMI')

df = bq.select.to_df(query='select * from tiktok2.users limit 1')

print(df)

