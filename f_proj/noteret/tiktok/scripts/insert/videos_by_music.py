from f_google.big_query.client import BigQuery
from f_proj.rapid_api.tiktok.api import TiktokAPI
from f_proj.noteret.tiktok.tables import Tables
from f_utils import u_datetime


def prod():
    bq = BigQuery()
    musics = bq.select.list(Tables.VIDEOS_BY_MUSIC_TODO)
    for i, id_music in enumerate(musics):
        tname = Tables.VIDEOS_BY_MUSIC
        rows = TiktokAPI.videos_from_music(id_music=id_music)
        bq.insert.rows_inserted(tname=tname, rows=rows)
        print(u_datetime.now(), f'[{i+1} / {len(musics)}]')


# t()
prod()
