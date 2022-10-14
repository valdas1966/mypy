from f_db.c_bq import BigQuery


json_key = '.json'

d = dict()
for i in range(1000000):
    print(i+1)
    d[i] = BigQuery(json_key)
for i in d:
    d[i].close()
