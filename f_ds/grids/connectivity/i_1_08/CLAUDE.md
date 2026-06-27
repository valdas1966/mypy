# Connectivity_8

## Purpose
8-connectivity (Moore): the 4 cardinals + 4 diagonals, **scaled-integer
octile** costs, and **strict no-corner-cutting**. The 2D twin of the
planned 3D 26-connectivity.

> Visual explainers (self-contained, open in a browser):
> - `octile_distance.html` — the octile distance.
> - `corner_cutting.html` — why a diagonal can be illegal even when its
>   destination is free (the strict both-flanks-free rule).

## Public API

### Properties
| Property | Value | Description |
|----------|-------|-------------|
| `offsets` | 8 deltas | Clockwise from N: N, NE, E, SE, S, SW, W, NW |
| `unit` | `10000` | `= COST_CARDINAL`; true distance = `cost / unit` |

### Methods
| Method | Returns | Description |
|--------|---------|-------------|
| `is_cardinal(a, b)` | `bool` | Inherited from base; classifies a move as cardinal vs diagonal — `cost` and `is_legal_move` both branch on it |
| `cost(a, b)` | `int` | `COST_DIAGONAL` if diagonal else `COST_CARDINAL` (via `is_cardinal`) |
| `distance(a, b)` | `int` | Scaled-integer octile: `DIAG·d_min + CARD·(d_max − d_min)`; admissible 8-conn heuristic (≠ `HasRowCol.distance` Manhattan, which is inadmissible here) |
| `is_legal_move(a, b, is_free)` | `bool` | Cardinal → always; diagonal → BOTH flanks free (via `is_free(row, col)`) |

## Constants
| Name | Scope | Value | Meaning |
|------|-------|-------|---------|
| `_OFFSETS` | class (private) | 8 deltas | Cardinals + diagonals, clockwise from N; read via the `offsets` property |
| `_COST_CARDINAL` | class (private) | `10000` | Straight-move cost; the scale unit (exposed via `unit`) |
| `_COST_DIAGONAL` | class (private) | `14142` | Diagonal-move cost; `round(√2 · 10000)` |

## Design Decisions
- **Scaled-int, not float √2** — keeps cost/distance comparisons exact
  (co-optimal ties for OMSPP / kA*). Same constants in `cost` and
  `distance` ⇒ admissible & consistent; exact on an obstacle-free grid.
- **Strict no-corner-cutting** — a diagonal `a → b` is illegal if either
  flank `(a.row, b.col)` / `(b.row, a.col)` is blocked (queried via the
  `is_free` predicate). Matches MovingAI / GPPC / JPS optimal costs.

## Inheritance
```
ConnectivityBase
 └── Connectivity_8
```

## Dependencies
- `f_ds.grids.connectivity.i_0_base.ConnectivityBase`
- `f_core.mixins.has.row_col.HasRowCol`
- `typing.Callable` — the `is_free` predicate (no grid type imported)

## Usage
```python
from f_ds.grids.connectivity import Connectivity_8

c = Connectivity_8()
c.cost(a=cell_0_0, b=cell_1_1)         # 14142  (diagonal)
c.distance(a=cell_0_0, b=cell_2_3)     # 38284
is_free = lambda row, col: (row, col) not in {(0, 0)}
c.is_legal_move(a=cell_1_0, b=cell_0_1, is_free=is_free)  # False: (0,0) blocked
```
