from f_google.big_query.client import BigQuery
from proj.rapid_api.c_tiktok import TikTok


def users_snapshots(rows: list[dict]) -> None:
    tname = 'noteret.tiktok.users_snapshots'
    BigQuery().insert.rows_inserted(tname=tname, rows=rows)


def followers(rows: list[dict]) -> None:
    tname = 'noteret.tiktok.followers'
    BigQuery().insert.rows_inserted(tname=tname, rows=rows)
