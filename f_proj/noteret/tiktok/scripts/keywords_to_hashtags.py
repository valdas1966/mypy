from f_proj.rapid_api.c_tiktok import TikTok
from f_google.services.big_query.client import BigQuery
from f_google.services.big_query.structures.schema import Schema


tname_input = 'noteret.tiktok2.keywords_to_hashtags_input'
tname_output = 'noteret.tiktok2.keywords_to_hashtags_output'


def create_table_input() -> None:
    schema = Schema()
    schema.add(name='keyword', dtype=Schema.STRING)
    BigQuery().create.table(tname=tname_input, schema=schema)

def create_table_output() -> None:
    schema = Schema()
    schema.add(name='keyword')
    schema.add(name='id')
    schema.add(name='name')
    schema.add(name='users', dtype=Schema.INTEGER)
    schema.add(name='inserted', dtype=Schema.DATETIME)
    BigQuery().create.table(tname=tname_output, schema=schema)

def insert_into_input() -> None:
    rows = [{'keyword': 'gaza'}]
    BigQuery().insert.rows(tname=tname_input, rows=rows)


def run() -> None:
    keywords = BigQuery().select.list(query=tname_input)
    t = TikTok()
    for i, keyword in enumerate(keywords):
        hashtags = t.keyword_to_hashtags(keyword=keyword)
        rows = [{**h._asdict(), 'keyword': keyword} for h in hashtags]
        BigQuery().insert.rows_inserted(tname=tname_output, rows=rows)
        print(f'Finished [{i+1}/{len(keywords)}] [{keyword}]')


# create_table_input()
# create_table_output()
# run()
# print(BigQuery().select.df(query=tname_output))
