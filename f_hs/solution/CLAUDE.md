# f_hs/solution — Search-Problem Solutions

## Purpose
Solution types for search problems. Each is a `SolutionAlgo`
subclass — `bool(sol)` returns the validity flag, no other
universal contract is imposed by the f_cs layer.

## Classes

| Class | Wraps | Used by |
|---|---|---|
| `SolutionSPP` | a single `cost` (float) | SPP algorithms (AStar, BFS, Dijkstra, AStarLookup) |
| `SolutionOMSPP` | `dict[State, SolutionSPP]` | OMSPP algorithms (KAStarAgg, KAStarInc) |

Path reconstruction is **not** on the Solution — it requires
the algorithm's parent-pointer state and lives on the Algo
(`algo.reconstruct_path(goal)`).

---

## SolutionSPP

### Constructor
```python
def __init__(self, cost: float) -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `cost` | `float` | The optimal path cost |
| `is_valid` (via `__bool__`) | `bool` | `cost < inf` |

### Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `valid()` | `SolutionSPP` | cost=5.0, is_valid=True |
| `invalid()` | `SolutionSPP` | cost=inf, is_valid=False |
| `zero()` | `SolutionSPP` | cost=0.0, is_valid=True |

---

## SolutionOMSPP

### Purpose
Per-goal solution wrapper for One-to-Many SPP. The algorithm
populates one `SolutionSPP` per requested goal (cost=`inf`
for unreachable goals); `SolutionOMSPP` exposes them as both
a Mapping and an f_cs SolutionAlgo.

### Constructor
```python
def __init__(self, per_goal: dict[State, SolutionSPP]) -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `per_goal` | `dict[State, SolutionSPP]` | Underlying `{goal: SolutionSPP}` map (copy) |
| `costs` | `dict[State, float]` | `{goal: cost}` view |
| `is_all_reached` | `bool` | True iff every cost is finite |
| `is_valid` (via `__bool__`) | `bool` | True iff non-empty |

### Mapping protocol
Behaves as a `collections.abc.Mapping`. Inherits:
`__getitem__`, `__iter__`, `__len__`, `__contains__`, `keys()`,
`values()`, `items()`, `get()`, `==` against other Mappings.

### MRO note
`SolutionOMSPP(SolutionAlgo, Mapping)`. `Validatable.__bool__`
wins over Mapping's len-based truthiness — `bool(sol) ==
sol.is_valid` (set by the validity flag at construction),
not `len(sol) > 0`. The two happen to agree under the current
constructor (is_valid = bool(per_goal) = (len > 0)) but the
contract is the validity flag, not the len.

---

## Design Decisions
- **Cost only on SPP** — path reconstruction belongs on the Algo.
- **is_valid for SPP** — `cost < inf`.
- **is_valid for OMSPP** — non-empty per-goal map (the
  algorithm guarantees one entry per requested goal, so
  is_valid effectively says "the algorithm completed and
  attempted every goal"). The stronger predicate is
  `is_all_reached` (every cost finite).
- **Mapping for OMSPP** — clients that already expect a dict
  (existing tests use `sol.items()`, `sol[goal]`, etc.)
  continue to work; clients that want the f_cs validity
  contract get it via `bool(sol)` / `is_all_reached`.

## Dependencies
- `f_cs.solution.SolutionAlgo`
- `collections.abc.Mapping`
