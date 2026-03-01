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
    tname = Tables.HASHTAGS_BY_KEYWORD    
    bq = BigQuery()
    rows: list[dict[str, Any]] = list()
    keywords: list[str] = bq.select.list(Tables.HASHTAGS_BY_KEYWORD_TODO)
    for keyword in keywords:
        rows_new = RequestsTiktok.hashtags_by_keyword(keyword=keyword)
        print(keyword, len(rows_new))
        rows.extend(rows_new)
        if len(rows) >= _BATCH_SIZE:
            bq.insert.rows_inserted(tname=tname, rows=rows)
            rows = list()
    if rows:
        bq.insert.rows_inserted(tname=tname, rows=rows)


prod()
