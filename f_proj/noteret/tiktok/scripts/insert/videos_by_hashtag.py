from f_google.services.big_query.client import BigQuery
from f_proj.rapid_api.tiktok.api import TiktokAPI
from f_proj.noteret.tiktok.tables import Tables
from f_utils import u_datetime


def prod():
    bq = BigQuery()
    hashtags = bq.select.list(Tables.VIDEOS_BY_HASHTAG_TODO)
    # hashtags = ['1653829802759174', '1598582492977158']
    for i, id_hashtag in enumerate(hashtags):
        print(f'{u_datetime.now()} Start working on hashtag: [{id_hashtag}] '
              f'[{i+1} / {len(hashtags)}]')
        tname = Tables.VIDEOS_BY_HASHTAG
        rows = TiktokAPI.videos_from_hashtag(id_hashtag=id_hashtag)
        if rows:
            try:
                bq.insert.rows_inserted(tname=tname, rows=rows)
                #print(u_datetime.now(), len(rows), f'[{i+1} /
                # {len(hashtags)}]')
            except Exception as e:
                print(str(e))
        else:
            print(u_datetime.now(), len(rows), f'[{i + 1} / {len(hashtags)}]')


# t()
prod()
