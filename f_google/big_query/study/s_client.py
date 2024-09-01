from f_google.big_query.client import BigQuery


bq = BigQuery(user='RAMI')

print(bq.user)
print(bq.creds)

