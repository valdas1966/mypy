from f_google.big_query.client import BigQuery
from f_google.big_query.structures.schema import Schema


bq = BigQuery(user='RAMI')

tname = 'noteret.tiktok2.test_insert_1'

"""
schema = Schema()
schema.add('a', Schema.INTEGER)
schema.add('b', Schema.STRING)
schema.add('inserted', Schema.DATETIME)
bq.create.table(tname=tname, schema=schema)
"""

rows = [{'a': '1'}]
bq.insert.rows_inserted(tname=tname, rows=rows)
