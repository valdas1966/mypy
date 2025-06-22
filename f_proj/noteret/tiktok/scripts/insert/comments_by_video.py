from old_f_google.services.big_query.client import BigQuery
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
    tname = Tables.COMMENTS_BY_VIDEO    
    bq = BigQuery()
    rows: list[dict[str, Any]] = list()
    ids_videos: list[str] = bq.select.list(Tables.COMMENTS_BY_VIDEO_TODO)
    for id_video in ids_videos:
        rows_new = RequestsTiktok.comments_by_video(id_video=id_video)
        print(id_video, len(rows_new))
        rows.extend(rows_new)
        if len(rows) >= _BATCH_SIZE:
            bq.insert.rows_inserted(tname=tname, rows=rows)
            rows = list()
    if rows:
        bq.insert.rows_inserted(tname=tname, rows=rows)


prod()
