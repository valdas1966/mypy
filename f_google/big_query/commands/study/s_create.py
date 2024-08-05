from f_google.big_query.client import BigQuery
from f_google.big_query.structures.schema import Schema

tname = 'noteret.tiktok2.temp_1'
schema = Schema()
schema.add('list', Schema.INTEGER)
schema.add('b', Schema.STRING)

bq = BigQuery(user='RAMI')
bq.create.table(tname=tname, schema=schema)
