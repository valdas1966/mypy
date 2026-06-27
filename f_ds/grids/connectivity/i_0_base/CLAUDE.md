# ConnectivityBase

## Purpose
Abstract connectivity policy for a 2D grid. Defines the surface every
connectivity implements: neighbor `offsets`, edge `cost`, admissible
`distance`, corner-cutting `is_legal_move`, and the `unit` scale.
Concrete subclasses are `Connectivity_4` / `Connectivity_8`.

## Public API

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `offsets` | `tuple[tuple[int, int], ...]` | Neighbor `(d_row, d_col)` deltas (override) |
| `unit` | `int` | Scale factor; true distance = `cost / unit` (default `1`) |

### Methods
| Method | Signature | Description |
|--------|-----------|-------------|
| `is_cardinal` | `(a, b) -> bool` | `True` if `a → b` is axis-aligned (`d_row == 0 or d_col == 0`), `False` if diagonal — concrete geometric helper, assumes `a, b` adjacent |
| `cost` | `(a, b) -> int` | Edge cost between adjacent cells (override) |
| `distance` | `(a, b) -> int` | Min obstacle-free path cost `a → b`; admissible/consistent heuristic. The movement-model metric — tracks the cost model, not a coord's tuple identity (override) |
| `is_legal_move` | `(a, b, is_free) -> bool` | Move legality; default `True` (cardinals never cut a corner) |

`a` / `b` are `Point2D` lattice coords (a bare `(row, col)` value with
no grid behavior — so `distance` can never collide with a stored
metric); `is_free(row, col) -> bool` reports cell
passability (supplied by the grid at call time) — so the policy imports
no grid type and stays below the grid in the dependency order.

## Inheritance
```
ConnectivityBase
 ├── Connectivity_4
 └── Connectivity_8
```

## Dependencies
- `f_ds.geometry.point2d.Point2D` — the lattice coordinate (`a`, `b`)
- `typing.Callable` — the `is_free` predicate

## Usage
```python
from f_ds.grids.connectivity import Connectivity_4

connectivity = Connectivity_4()
connectivity.offsets          # ((-1,0), (0,1), (1,0), (0,-1))
connectivity.unit             # 1
```
