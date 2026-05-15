# `f_psl/builtins/list` — List Utilities

## 1) Purpose
Static utility class `UList` grouping helpers that operate on
the built-in `list` type. Lives under `f_psl/builtins/` because
`list` is exposed by the Python `builtins` stdlib module.

## 2) Public API

### `UList` (`main.py`)
- `UList.sliding_windows(li: list, size: int) -> list[list]`
  Return all sliding windows of `size` consecutive elements over
  `li`, in order. For `N = len(li)` and `K = size` (with
  `K >= 1`), produces `N - K + 1` windows; returns `[]` when
  `K > N`. Example:
  `sliding_windows(li=[1, 2, 3], size=2) -> [[1, 2], [2, 3]]`.

## 3) Inheritance (Hierarchy)
`UList` is a stand-alone **static utility class** (no instances,
no base). Follows the `U`-prefix convention.

## 4) Dependencies
- None (pure Python lists).

## 5) Usage Example
```python
from f_psl.builtins.list import UList

UList.sliding_windows(li=[1, 2, 3, 4], size=2)
# [[1, 2], [2, 3], [3, 4]]
```

## Files
| File | Purpose |
|------|---------|
| `main.py` | `UList` class. |
| `__init__.py` | Re-exports `UList`. |
| `_tester.py` | Single pytest test bundling all asserts. |
