from old_old_f_google.services.big_query.client import BigQuery
from f_proj.rapid_api.tiktok.requests import RequestsTiktok
from f_proj.noteret.tiktok.tables import Tables
from typing import Any


_BATCH_SIZE = 1000


def prod() -> None:
    """
    ========================================================================
     Insert into BigQuery [ ].
    ========================================================================
    """
    tname = Tables.VIDEOS_BY_HASHTAG    
    bq = BigQuery()
    rows: list[dict[str, Any]] = list()
    ids_hashtags: list[str] = bq.select.list(Tables.VIDEOS_BY_HASHTAG_TODO)
    for id_hashtag in ids_hashtags:
        rows_new = RequestsTiktok.videos_by_hashtag(id_hashtag=id_hashtag)
        print(id_hashtag, len(rows_new))
        rows.extend(rows_new)
        if len(rows) >= _BATCH_SIZE:
            bq.insert.rows_inserted(tname=tname, rows=rows)
            rows = list()
    if rows:
        bq.insert.rows_inserted(tname=tname, rows=rows)


prod()
