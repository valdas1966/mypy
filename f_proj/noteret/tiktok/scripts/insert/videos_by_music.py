from old_old_f_google.services.big_query.client import BigQuery
from f_proj.rapid_api.tiktok.requests import RequestsTiktok
from f_proj.noteret.tiktok.tables import Tables
from typing import Any


_BATCH_SIZE = 1000


def prod() -> None:
    """
    ========================================================================
     Insert into BigQuery [videos by user].
    ========================================================================
    """
    tname = Tables.VIDEOS_BY_MUSIC
    bq = BigQuery()
    rows: list[dict[str, Any]] = list()
    ids_musics: list[str] = bq.select.list(Tables.VIDEOS_BY_MUSIC_TODO)
    for id_music in ids_musics:
        rows_new = RequestsTiktok.videos_by_music(id_music=id_music)
        print(id_music, len(rows_new))
        rows.extend(rows_new)
        if len(rows) >= _BATCH_SIZE:
            bq.insert.rows_inserted(tname=tname, rows=rows)
            rows = list()
    if rows:
        bq.insert.rows_inserted(tname=tname, rows=rows)


prod()
