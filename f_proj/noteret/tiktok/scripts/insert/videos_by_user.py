from f_google.services.big_query.client import BigQuery
from f_proj.rapid_api.tiktok.api_new import TiktokAPI
from f_proj.noteret.tiktok.tables import Tables
from typing import Any


_BATCH_SIZE = 10


def prod() -> None:
    """
    ========================================================================
     Insert into BigQuery [videos by user].
    ========================================================================
    """
    tname = Tables.VIDEOS_BY_USER
    bq = BigQuery()
    rows: list[dict[str, Any]] = list()
    ids_users: list[str] = bq.select.list(Tables.VIDEOS_BY_USER_TODO)
    for id_user in ids_users:
        rows_new = TiktokAPI.videos_by_user(id_user=id_user)
        print(id_user, len(rows_new))
        rows.extend(rows_new)
        if len(rows) >= _BATCH_SIZE:
            bq.insert.rows_inserted(tname=tname, rows=rows)
            rows = list()
    if rows:
        bq.insert.rows_inserted(tname=tname, rows=rows)


prod()
