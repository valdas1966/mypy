# BigQuery

## Purpose
Client wrapper for Google BigQuery.
Provides DataFrame-based queries, DDL/DML execution, and table management.

## Public API

### `__init__(creds: SACredentials) -> None`
Create a BigQuery client with Service-Account credentials.

### `select(query: str, limit: int = -1) -> pd.DataFrame`
Run a SELECT query, return results as DataFrame.
If `query` has no spaces, treated as a table name (`SELECT * FROM {query}`).

### `select_list(query: str, col: str = None) -> list[str]`
Return a single column as `list[str]`. Uses first column if `col` is None.

### `select_value(query: str) -> any`
Return the first cell value (row 0, col 0).

### `run(command: str) -> None`
Execute a DDL/DML command.

### `create(tname: str, cols: list[str]) -> None`
Create a table (drops if exists). Cols format: `['name string', 'age int64']`.

### `insert_rows(tname: str, rows: list[dict]) -> None`
Batch insert rows into a table.

### `count(tname: str) -> int`
Return number of rows in a table.

### `is_exists(tname: str) -> bool`
Return True if the table exists.

### `drop(tname: str) -> None`
Drop a table if it exists.

### `cols(tname: str) -> list[str]`
Return column names of a table.

### `close() -> None`
Close the BigQuery client connection.

## Inheritance (Hierarchy)
```
BigQuery (no base class)
```
No inheritance. Standalone client wrapper.

## Dependencies

| Import | Purpose |
|--------|---------|
| `google.oauth2.service_account.Credentials` | SA credentials |
| `google.cloud.bigquery` | BigQuery client |
| `pandas` | DataFrame results |

## Usage Example
```python
from f_google.bigquery import BigQuery

bq = BigQuery.Factory.rami()
df = bq.select(query='noteret.dataset.table', limit=10)
count = bq.count(tname='noteret.dataset.table')
bq.close()
```
