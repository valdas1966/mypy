from f_google.services.big_query.client import BigQuery
from f_proj.rapid_api.tiktok.api_new import TiktokAPI
from f_proj.noteret.tiktok.tables import Tables
from typing import Any


_BATCH_SIZE = 10


def prod() -> None:
    """
    ========================================================================
     Insert into BigQuery [users by id].
    ========================================================================
    """
    tname = Tables.USERS_BY_ID
    bq = BigQuery()
    rows: list[dict[str, Any]] = list()
    ids_users: list[str] = bq.select.list(Tables.USERS_BY_ID_TODO)
    for id_user in ids_users:
        row = TiktokAPI.users_by_id(id_user=id_user)
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
    ids_users: list[str] = ['107955']
    for id_user in ids_users:
        row = TiktokAPI.users_by_id(id_user=id_user)
        print(id_user, row)


# study()
prod()
