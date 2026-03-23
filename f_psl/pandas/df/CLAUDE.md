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
| `add_col_agg(df, cols, col, func)` | Add a column by aggregating values across specified columns per row using the given function (e.g., `min`, `max`, `sum`). |
| `union(df_1, df_2)` | Union two DataFrames with the same columns (UNION ALL, `ignore_index=True`). |
| `add_col_bins(df, col, bins=None, n=None)` | Add `binned_{col}` column by snapping values to nearest bin. Provide explicit `bins` or `n` to auto-generate. Delegates to `UArray.snap_to_bins`. |
