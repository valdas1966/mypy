# `f_psl/builtins` — Built-in Type Utilities

## 1) Purpose
Aggregator package for static utility classes wrapping Python
**built-in types** (`list`, future `dict`, `str`, `set`,
`tuple`, `int`, `bool`). Each type gets its own subpackage with
a `U<Type>` static utility class.

## 2) Public API
Lazy re-exports via `ULazy.install()` (`f_core.imports`) —
importing one class does not load sibling subpackages.

| Symbol | Source |
|--------|--------|
| `UList` | `f_psl.builtins.list` |

## 3) Inheritance (Hierarchy)
None — pure aggregator. Subpackage classes are stand-alone
`U`-prefix static utilities.

## 4) Dependencies
- None.

## 5) Usage Example
```python
from f_psl.builtins import UList

UList.sliding_windows(li=[1, 2, 3, 4], size=2)
# [[1, 2], [2, 3], [3, 4]]
```

## Files
| File | Purpose |
|------|---------|
| `__init__.py` | `ULazy.install()` lazy aggregator (2 lines). |
| `list/` | `UList` — built-in `list` utilities. |
