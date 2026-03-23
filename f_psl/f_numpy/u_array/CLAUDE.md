# f_psl/f_numpy/u_array

## Purpose
Static utility class for NumPy array operations.

## Class: UArray

### Methods
| Method | Description |
|--------|-------------|
| `remove_empty_rows(array)` | Remove empty rows from a numpy array. |
| `remove_empty_columns(array)` | Remove empty columns from a numpy array. |
| `remove_empty_rows_and_columns(array)` | Remove empty rows and columns from a numpy array. |
| `generate_bins(values, n)` | Generate `n` evenly-spaced integer bins spanning the range of `values`. Uses `np.linspace` + round. |
| `snap_to_bins(values, bins)` | Snap each value to the nearest bin. Ties go to lower bin. Uses `np.searchsorted` for O(n log k) performance. |
