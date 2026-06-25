# ConnectivityBase

## Purpose
Abstract connectivity policy for a 2D grid. Defines the surface every
connectivity implements: neighbor `offsets`, edge `cost`, admissible
`heuristic`, corner-cutting `is_legal_move`, and the `unit` scale.
Concrete subclasses are `Connectivity4` / `Connectivity8`.

## Public API

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `offsets` | `tuple[tuple[int, int], ...]` | Neighbor `(d_row, d_col)` deltas (override) |
| `unit` | `int` | Scale factor; true distance = `cost / unit` (default `1`) |

### Methods
| Method | Signature | Description |
|--------|-----------|-------------|
| `cost` | `(a, b) -> int` | Edge cost between adjacent cells (override) |
| `heuristic` | `(a, b) -> int` | Admissible lower-bound cost `a → b` (override) |
| `is_legal_move` | `(a, b, is_free) -> bool` | Move legality; default `True` (cardinals never cut a corner) |

`a` / `b` are any `HasRowCol`; `is_free(row, col) -> bool` reports cell
passability (supplied by the grid at call time) — so the policy imports
no grid type and stays below the grid in the dependency order.

## Inheritance
```
ConnectivityBase
 ├── Connectivity4
 └── Connectivity8
```

## Dependencies
- `f_core.mixins.has.row_col.HasRowCol`
- `typing.Callable` — the `is_free` predicate

## Usage
```python
from f_ds.grids.connectivity import Connectivity4

connectivity = Connectivity4()
connectivity.offsets          # ((-1,0), (0,1), (1,0), (0,-1))
connectivity.unit             # 1
```
