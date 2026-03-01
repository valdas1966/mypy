from old_old_f_google.services.big_query.client import BigQuery

bq = BigQuery(user='RAMI')

tname = 'noteret.tiktok2.test_insert_1'

"""
schema = Schema()
schema.add('list', Schema.INTEGER)
schema.add('b', Schema.STRING)
schema.add('inserted', Schema.DATETIME)
bq.create.table(tname=tname, schema=schema)
"""

rows = [{'list': '1'}]
bq.insert.rows_inserted(tname=tname, rows=rows)
