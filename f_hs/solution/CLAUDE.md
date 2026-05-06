# f_hs/solution — Search-Problem Solutions

## Purpose
Solution types for the SPP family. Each is a `SolutionAlgo`
subclass — `bool(sol)` returns the validity flag; no other
universal contract is imposed by the f_cs layer.

## Classes

| Class | Wraps | Used by |
|---|---|---|
| `SolutionSPP` | a single `cost` (float) | OOSPP algorithms (AStar, BFS, Dijkstra, AStarLookup) |
| `SolutionPerKey[Key, Val]` | `dict[Key, Val]` (abstract spine) | shared base for `SolutionOMSPP`, `SolutionMOSPP`, future `SolutionMMSPP` |
| `SolutionOMSPP` | `dict[goal-State, SolutionSPP]` | OMSPP algorithms (KAStarAgg, KAStarInc) |
| `SolutionMOSPP` | `dict[start-State, SolutionSPP]` | MOSPP algorithms (k×A*, k×A*-CB; symmetric to OMSPP) |

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
| `__bool__` | `bool` | `cost < inf` |

### Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `valid()` | `SolutionSPP` | cost=5.0, valid |
| `invalid()` | `SolutionSPP` | cost=inf, invalid |
| `zero()` | `SolutionSPP` | cost=0.0, valid |

---

## SolutionPerKey[Key, Val]  (abstract spine)

Lives in `f_hs/solution/per_key.py`. Wraps a `dict[Key, Val]`
where `Val` is itself a `SolutionAlgo` (a leaf `SolutionSPP`,
or a nested per-key wrapper).

### Constructor
```python
def __init__(self, per_key: dict[Key, Val]) -> None
```

### Mapping protocol
Behaves as a `collections.abc.Mapping` over the wrapped dict.
Inherits: `__getitem__`, `__iter__`, `__len__`, `__contains__`,
`keys()`, `values()`, `items()`, `get()`, `==` against other
Mappings.

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `__bool__` | `bool` | True iff the wrapper is non-empty |
| `is_all_reached` | `bool` | True iff every Val is "reached". Recurses into nested per-key wrappers via their own `is_all_reached`; falls back to `bool(val)` for leaf `SolutionSPP` (where `bool` ⇔ `cost < inf`) |

### MRO
`SolutionPerKey(SolutionAlgo, Mapping, Generic[Key, Val])`.
`Validatable.__bool__` (via SolutionAlgo) wins over Mapping's
len-based truthiness — `bool(sol)` is the validity flag set
at construction, not `len(sol) > 0`. The two happen to agree
under this constructor (`is_valid = bool(per_key)`) but the
contract is the validity flag.

---

## SolutionOMSPP

Solution for the **One-to-Many** SPP — one start, k goals.

### Constructor
```python
def __init__(self, per_goal: dict[State, SolutionSPP]) -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `per_goal` | `dict[State, SolutionSPP]` | Underlying `{goal: SolutionSPP}` map |
| `costs` | `dict[State, float]` | `{goal: cost}` view |
| `is_all_reached` | `bool` | (inherited) True iff every goal is reached |
| `__bool__` | `bool` | True iff non-empty |

---

## SolutionMOSPP

Solution for the **Many-to-One** SPP — k starts, one goal.
Symmetric to `SolutionOMSPP` over the Key=start axis.

### Constructor
```python
def __init__(self, per_start: dict[State, SolutionSPP]) -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `per_start` | `dict[State, SolutionSPP]` | Underlying `{start: SolutionSPP}` map |
| `costs` | `dict[State, float]` | `{start: cost}` view |
| `is_all_reached` | `bool` | (inherited) True iff goal is reachable from every start |
| `__bool__` | `bool` | True iff non-empty |

---

## Design Decisions
- **Cost only on `SolutionSPP`** — path reconstruction is on
  the Algo (parent pointers live there).
- **Shared `SolutionPerKey` spine** — Mapping protocol +
  validity + `is_all_reached` recursion live once. OMSPP /
  MOSPP / future MMSPP each subclass and add a
  domain-specific alias (`per_goal` / `per_start`) and a
  `costs` view.
- **`is_all_reached` recurses generically** — `getattr(val,
  'is_all_reached', bool(val))`. Works for leaf
  `SolutionSPP` (falls back to `bool` ⇔ `cost < inf`) and
  for nested wrappers (recurses). MMSPP-ready without a
  spine change.
- **Symmetric naming** — `SolutionMOSPP.per_start` mirrors
  `SolutionOMSPP.per_goal`. Both keep their domain-specific
  alias rather than collapsing to a single generic name —
  reads better in algorithm code.

## Dependencies
- `f_cs.solution.SolutionAlgo` (validity contract)
- `collections.abc.Mapping` (protocol for the multi-classes)
- `f_hs.state.i_0_base.StateBase` (generic State bound)
