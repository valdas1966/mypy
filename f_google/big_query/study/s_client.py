from f_google.big_query.client import ClientBigQuery


bq = ClientBigQuery(user='RAMI')

print(bq.user)
print(bq.creds)