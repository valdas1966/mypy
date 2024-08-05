from f_db.c_bq import BigQuery
from google.cloud import bigquery
import json


json_key = 'd:\\tiktok2\\repo\\viewer.json'
bq = BigQuery(json_key=json_key)

def insert_rows():
    bq = BigQuery(json_key=json_key)
    tname = 'noteret.tiktok2.temp_0'
    rows = [{'list': 1, 'c': 'b'}]
    bq.insert_rows(tname=tname, rows=rows)
    bq.close()


def load_from_json():
    tname = 'noteret.tiktok2.temp_0'
    str_json = '{"list": 5}'
    bq = BigQuery(json_key=json_key)
    bq.insert_into_from_json(str_json=str_json, tname=tname)
    bq.close()


def insert_rows_json():
    tname = 'noteret.tiktok2.temp_logger'
    rows = [{'tries': 3, 'b': 4}]
    bq = BigQuery(json_key=json_key)
    bq.insert_rows_json(rows=rows, tname=tname)
    bq.close()


def insert_if_not_exist():
    tname_a = 'noteret.tiktok2.temp_2'
    tname_b = 'noteret.tiktok2.logger'
    bq.insert_if_not_exist(tname_a=tname_a, tname_b=tname_b)


def insert_into():
    tname = 'noteret.tiktok2.temp_0'
    bq = BigQuery(json_key=json_key)
    bq.insert_into(tname_from=tname, tname_to=tname)
    bq.close()


def count_duplicate_rows():
    tname = 'noteret.tiktok2.logger'
    print(bq.count_duplicate_rows(tname=tname, limit=1))


#load_from_json()
#insert_rows_json()
insert_if_not_exist()
#insert_into()
#count_duplicate_rows()

bq.close()
