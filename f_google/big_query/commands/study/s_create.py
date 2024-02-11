from f_google.big_query.client import ClientBigQuery
from f_google.big_query.structures.schema import Schema

tname = 'noteret.tiktok2.temp_1'
schema = Schema()
schema.add('a', Schema.INTEGER)
schema.add('b', Schema.STRING)

bq = ClientBigQuery(user='RAMI')
bq.create.table(name=tname, schema=schema)
