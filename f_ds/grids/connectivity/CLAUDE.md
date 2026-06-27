# f_ds/grids/connectivity — Grid Connectivity Policies

## Purpose
Swappable **connectivity policy** for a 2D grid. One object carries the
four things that change with connectivity: neighbor **offsets**, edge
**cost**, admissible **distance**, and corner-cutting **legality**. The
grid holds a policy and delegates to it, so 4-conn ↔ 8-conn becomes a
constructor choice instead of a code fork (and the same base extends to
3D 6/18/26-conn later).

Step 1 of the 8-connectivity migration: the policy classes only. Wiring
into `GridMap` / `ProblemGrid` / the A* heuristic is a later step — this
package changes no existing behavior.

## Package Exports
```python
from f_ds.grids.connectivity import (
    ConnectivityBase, Connectivity_4, Connectivity_8,
)
```

## Module Structure
```
connectivity/
├── __init__.py     ConnectivityBase, Connectivity_4, Connectivity_8 (ULazy)
├── i_0_base/       ConnectivityBase — abstract policy
├── i_1_04/       Connectivity_4 — 4-conn (von Neumann), legacy behavior
└── i_1_08/      Connectivity_8 — 8-conn (Moore), scaled-int octile
                    (3D later: i_1_06 / i_1_18 / i_1_26)
```

## Inheritance
```
ConnectivityBase
 ├── Connectivity_4
 └── Connectivity_8
```

## Policy Surface
| Member | Connectivity_4 | Connectivity_8 |
|--------|---------------|---------------|
| `is_cardinal(a,b)` | shared (base) — `True` iff `d_row == 0 or d_col == 0` | shared (base) — drives `cost` / `is_legal_move` |
| `offsets` | 4 cardinals (N,E,S,W) | + 4 diagonals (8 total) |
| `cost(a,b)` | `1` | `10000` cardinal / `14142` diagonal |
| `distance(a,b)` | Manhattan | scaled-int octile |
| `is_legal_move(a,b,is_free)` | `True` | diagonal ⇔ both flanks free |
| `unit` | `1` | `10000` (true dist = `cost / unit`) |

## Design Decisions
- **Scaled-int octile, not float √2.** Cardinal `10000`, diagonal
  `14142` keep every cost/distance comparison exact — required for
  OMSPP / kA* co-optimal tie detection, which float rounding corrupts.
  Same constants in `cost` and `distance` ⇒ admissible and consistent.
- **Strict no-corner-cutting.** A diagonal is legal only when BOTH
  flank cells are free — matches MovingAI / GPPC / JPS released
  optimal costs.
- **No `f_core` change.** The policy lives in `f_ds/grids` and operates
  on any `HasRowCol`; the `HasRowCol` mixin stays identity-only.
- **Imports no grid type.** `is_legal_move` takes an `is_free(row, col)`
  predicate (supplied by the grid), instead of a `GridMap`. Corner-cutting
  is the only validity-dependent method — and validity is a `GridMap`
  concept, not `GridBase`. The predicate keeps the policy *below* the grid
  in the dependency order and grid-agnostic (2D maps ↔ 3D voxels alike).

## Dependencies
- `f_core.mixins.has.row_col.HasRowCol` — cell row/col accessor
- `f_core.imports.ULazy` — lazy aggregator
- `typing.Callable` — the `is_free` predicate (no grid type imported)
