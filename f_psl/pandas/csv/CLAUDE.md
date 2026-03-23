# f_psl/pandas/csv

## Purpose
Pandas-powered CSV file operations. Composes `UDf` methods
for file-to-file pipelines.

## Class: UCsv

### Methods
| Method | Description |
|--------|-------------|
| `group(path_input, path_output, col_a, col_b, agg='mean')` | Read CSV, group `col_b` by `col_a`, write result to CSV. `col_b` accepts `str` or `list[str]`. If `col_a`/`col_b` are None, uses 1st/2nd columns. |
| `add_col_agg(path, cols, col, func)` | Read CSV, add a column by aggregating values across specified columns per row using a Callable, write back. |
| `union(path_1, path_2, path_output)` | Read two CSVs, union them (UNION ALL), write result to output CSV. |
| `add_col_bins(path, col, bins=None, n=None)` | Read CSV, add `binned_{col}` column by snapping values to nearest bin, write back. |

### Dependencies
- `f_psl.pandas.df.UDf` — for `read()`, `group()`, `write()`.
