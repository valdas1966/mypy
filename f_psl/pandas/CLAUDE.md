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
| `add_comparing_cols(df, col_a, col_b)` | Compare two columns row-by-row, add `min`/`pct`/`oracle` columns. |

### UCsv (csv/)
Static utility class for pandas-powered CSV file operations.

| Method | Description |
|--------|-------------|
| `group(path_input, path_output, col_a, col_b, agg='mean')` | Read CSV, group col_b by col_a, write result to CSV. |
| `add_comparing_cols(path, col_a, col_b)` | Read CSV, compare two columns, add `min`/`pct`/`oracle` columns, write back. |
