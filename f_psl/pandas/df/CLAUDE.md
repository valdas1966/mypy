# f_psl/pandas/df

## Purpose
Static utility class for pandas DataFrame operations.

## Class: UDf

### Methods
| Method | Description |
|--------|-------------|
| `read(path)` | Read a CSV file into a DataFrame. |
| `write(df, path)` | Write a DataFrame to a CSV file (no index). |
| `group(df, col_a, col_b, agg='mean')` | Group `col_b` by `col_a` with aggregation. `col_b` accepts `str` or `list[str]` for multi-column grouping. If `col_a`/`col_b` are None, uses 1st/2nd columns. `agg` accepts pandas strings: `'mean'`, `'sum'`, `'count'`, `'min'`, `'max'`, `'median'`. |
| `add_comparing_cols(df, col_a, col_b)` | Compare two columns row-by-row. Adds `min` (name of column with lower value or `'equals'`), `pct` (savings ratio `(max-min)/max` in [0,1]), and `oracle` (min value of the two). |
