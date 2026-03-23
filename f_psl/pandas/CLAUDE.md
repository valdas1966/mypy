# f_psl/pandas

## Purpose
Pandas DataFrame and CSV utility wrappers. Replaces `f_psl/old_pandas`.

## Structure
```
f_psl/pandas/
├── df/          # UDf — DataFrame utility class
└── csv/         # UCsv — pandas-powered CSV file operations
```

## Classes

### UDf (df/)
Static utility class for pandas DataFrame operations.

| Method | Description |
|--------|-------------|
| `read(path)` | Read a CSV file into a DataFrame. |
| `write(df, path)` | Write a DataFrame to a CSV file (no index). |
| `group(df, col_a, col_b, agg='mean')` | Group `col_b` by `col_a` with aggregation. If `col_a`/`col_b` are None, uses 1st/2nd columns. |
| `add_col_agg(df, cols, col, func)` | Add a column by aggregating values across specified columns per row using a Callable. |
| `union(df_1, df_2)` | Union two DataFrames with the same columns (UNION ALL). |
| `add_col_bins(df, col, bins=None, n=None)` | Add `binned_{col}` column by snapping values to nearest bin. |

### UCsv (csv/)
Static utility class for pandas-powered CSV file operations.

| Method | Description |
|--------|-------------|
| `group(path_input, path_output, col_a, col_b, agg='mean')` | Read CSV, group col_b by col_a, write result to CSV. |
| `add_col_agg(path, cols, col, func)` | Read CSV, add a column by aggregating values across specified columns per row, write back. |
| `union(path_1, path_2, path_output)` | Read two CSVs, union them (UNION ALL), write to output CSV. |
| `add_col_bins(path, col, bins=None, n=None)` | Read CSV, add `binned_{col}` column, write back. |
