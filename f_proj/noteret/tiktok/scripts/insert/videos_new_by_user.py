from old_f_google.services.big_query.client import BigQuery
from f_proj.rapid_api.tiktok.requests import RequestsTiktok
from f_proj.noteret.tiktok.tables import Tables
from typing import Any


_BATCH_SIZE = 1000


def prod() -> None:
    """
    ========================================================================
     Insert into BigQuery [videos new by user].
    ========================================================================
    """
    tname = Tables.VIDEOS_NEW_BY_USER
    bq = BigQuery()
    rows: list[dict[str, Any]] = list()
    df_todo = bq.select.df(Tables.VIDEOS_NEW_BY_USER_TODO)
    inputs = len(df_todo)
    # df_todo have 2 cols (id_user, created)
    for i, (id_user, created) in enumerate(df_todo.values):
        rows_new = RequestsTiktok.videos_new_by_user(id_user=id_user,
                                                created=created)
        print(f'[{i+1} / {inputs}] | '
              f'Id_User=[{id_user}] | '
              f'Last_Created=[{created}] | '
              f'Videos_New=[{len(rows_new)}]')
        rows.extend(rows_new)
        if len(rows) >= _BATCH_SIZE:
            bq.insert.rows_inserted(tname=tname, rows=rows)
            rows = list()
    if rows:
        bq.insert.rows_inserted(tname=tname, rows=rows)


prod()
