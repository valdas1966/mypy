from f_google.services.bigquery import BigQuery
from f_core.processes.i_3_parallel import ProcessParallel
from typing import Any, Callable


_BATCH_SIZE = 1000


def insert_parallel(tname: str,
                    tname_todo: str,
                    func: Callable[..., list[dict[str, Any]]],
                    workers: int = 5) -> None:
    """
    ========================================================================
     Fetch TODO args from BigQuery, call func per row in parallel,
     and batch-insert the resulting rows.
    ========================================================================
    """
    bq = BigQuery.Factory.rami()
    df = bq.select(query=tname_todo)
    if df.empty:
        print('No TODOs found')
        return
    # Convert DataFrame rows to list of tuples
    args_list: list[tuple[str, ...]] = [tuple(str(v) for v in row)
                                        for row in df.values]

    def fetch_chunk(chunk: list[tuple[str, ...]]) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch rows for a chunk of args.
        ====================================================================
        """
        rows: list[dict[str, Any]] = list()
        for args in chunk:
            rows_new = func(*args)
            print(args, len(rows_new))
            rows.extend(rows_new)
        return rows

    proc = ProcessParallel(input=args_list,
                           func=fetch_chunk,
                           workers=workers)
    results = proc.run()
    # Flatten results
    rows: list[dict[str, Any]] = list()
    for chunk_rows in results:
        if chunk_rows:
            rows.extend(chunk_rows)
    # Batch insert
    for i in range(0, len(rows), _BATCH_SIZE):
        batch = rows[i:i + _BATCH_SIZE]
        bq.insert_rows(tname=tname, rows=batch)
    # Log errors
    for idx, chunk_data, exc in proc.errors:
        print(f'Error in chunk {idx}: {exc}')
    print(f'Inserted {len(rows)} rows into {tname}')
