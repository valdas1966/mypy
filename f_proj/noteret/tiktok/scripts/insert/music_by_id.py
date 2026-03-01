from old_old_f_google.services.big_query.client import BigQuery
from f_proj.rapid_api.tiktok.requests import RequestsTiktok
from f_proj.noteret.tiktok.tables import Tables
from typing import Any


_BATCH_SIZE = 1000


def prod() -> None:
    """
    ========================================================================
     Insert into BigQuery [music by id].
    ========================================================================
    """
    tname = Tables.MUSIC_BY_ID
    bq = BigQuery()
    rows: list[dict[str, Any]] = list()
    ids_musics: list[str] = bq.select.list(Tables.MUSIC_BY_ID_TODO)
    for id_music in ids_musics:
        row = RequestsTiktok.music_by_id(id_music=id_music)
        rows.append(row)
        if len(rows) == _BATCH_SIZE:
            bq.insert.rows_inserted(tname=tname, rows=rows)
            rows = list()
    if rows:
        bq.insert.rows_inserted(tname=tname, rows=rows)


def study() -> None:
    """
    ========================================================================
     Study the data.
    ========================================================================
    """
    ids_musics: list[str] = ['7002634556977908485']
    for id_music in ids_musics:
        row = RequestsTiktok.music_by_id(id_music=id_music)
        print(id_music, row)


# study()
prod()
