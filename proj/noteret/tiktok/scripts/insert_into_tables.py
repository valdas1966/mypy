from f_google.big_query.client import BigQuery
from proj.rapid_api.c_tiktok import TikTok


def followers(id_user: str) -> None:
    tname = 'noteret.tiktok.temp_followers'
    t = TikTok()
    rows = t.user.followers(id_user=id_user)
    bq = BigQuery()
    bq.insert.rows_inserted(tname=tname, rows=rows)


followers(id_user='107955')
