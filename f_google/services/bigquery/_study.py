from f_google.services.bigquery import BigQuery


bq = BigQuery.Factory.rami()
df = bq.select('noteret.tiktok.hashtags_bibi')
bq.close()
print(df)
