# HBounded

## Purpose
Heuristic Source wrapping a base `HBase` with a frozen
`dict[State, float]` of admissible lower bounds. On a hit the
effective h is `max(base(state), bounds[state])`; on a miss the
base is used directly. Bounds are admissible but NOT perfect —
they shrink A*'s search space by tightening h without enabling
early-termination or path-stitching.

## Static-bounds Decision (2026-04-20)
- Bounds are **static for the lifetime of this object**. The
  constructor takes a defensive shallow copy; no mutation API.
  Mirrors `HCached`'s static-cache decision.
- Composable via wrapping: `HCached(base=HBounded(base=HCallable
  (fn), bounds={...}), cache={...}, goal=g)` — cache wins on
  hit, else bounded-max, else the base callable.

## Admissibility Contract
`bound[s] <= h*(s)` for every bounded state. Caller's
responsibility — **not enforced at runtime**. A cheap runtime
check against h* doesn't exist in general. Supplying a bound
greater than h\*(s) silently breaks A*'s optimality guarantee.

## Public API

### Constructor
```python
def __init__(self,
             base: HBase[State],
             bounds: dict[State, float]) -> None
```

### `__call__(state) -> float`
Returns `max(self._base(state), self._bounds[state])` on hit;
`self._base(state)` on miss.

### `is_perfect(state) -> bool`
Inherits `False` from HBase — always False. Bounded states do
NOT trigger `_early_exit` in AStar; they're just tighter h
values.

### `is_bounded(state) -> bool`
Overrides HBase. Returns True **iff** `bounds[state]` exists
AND is **strictly greater** than `base(state)`. Misses and
ties both return False — only strict improvements over base
count as "bound-tightened." Drives the `is_bounded=True` flag
on push / pop events in AStar's recorder.

Strict semantics chosen for parallel with `HCached.is_perfect`:
each flag's presence on a recorded event unambiguously means
"the specialized source determined h." A weaker-than-base
bound is NOT flagged (the base won; the bound had no effect).

### `suffix_next(state) -> State | None`
Inherits `None` from HBase — always None. Bounds carry no path
info.

### `add_bound(state, value) -> bool`
Insert `value` as a bound at `state` **iff** it strictly
tightens the current effective h: `value > self(state)`. On a
strict win, overwrites (or inserts) and returns True. On a tie
or weaker value, no-op returns False.

**Pre-search propagation only.** This is the one narrow
relaxation of the static-bounds invariant — the constructor
still takes a defensive shallow copy, and no other public
mutation exists. `add_bound` is consumed exclusively by
`AStar.propagate_pathmax` (Phase 2b), which runs as a setup
step before the search loop; during the search, bounds remain
effectively static.

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `bounds` | `dict[State, float]` | Read-only shallow copy |

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `graph_abc_tight()` | `HBounded` | base=0, bounds={A:2, B:1} |
| `graph_abc_weaker_than_base()` | `HBounded` | base(A)=2, bound[A]=1; base wins on max |

## Inheritance
```
HBase[State]
  └── HBounded[State]
```

## Tests
`_tester.py` — 12 contract tests:
1. `test_call_hit_returns_max_of_base_and_bound` — bound wins when > base.
2. `test_call_hit_returns_base_when_bound_weaker` — base wins when > bound.
3. `test_call_miss_delegates_to_base` — off-bounds delegation.
4. `test_is_perfect_always_false` — no early-exit for bounded states.
5. `test_suffix_next_always_none` — no path info.
6. `test_is_bounded_true_when_bound_tightens` — strict > base → True.
7. `test_is_bounded_false_when_bound_weaker` — bound < base → False.
8. `test_is_bounded_false_on_miss` — state not in bounds → False.
9. `test_is_bounded_false_when_bound_equals_base` — ties → False (strict).
10. `test_add_bound_tightens_returns_true` — strict win mutates + returns True.
11. `test_add_bound_no_op_when_not_tightening_returns_false` — tie / weaker → no-op False.
12. `test_constructor_takes_defensive_copy` — static-bounds guard.

## AStar Integration
Plug in as the `h` kwarg:
```python
from f_hs.heuristic.i_1_bounded import HBounded
from f_hs.heuristic.i_1_callable import HCallable

h = HBounded(
    base=HCallable(fn=lambda s: float(s.distance(goal))),
    bounds={some_state: tight_h_value},
)
algo = AStar(problem=problem, h=h)
```

Zero AStar edits — `_priority(state)` already routes through
`self._h(state)`. `cache_rank` stays 1 (is_perfect=False), so
the tie-break ordering is unchanged.

## Dependencies
- `f_hs.heuristic.i_0_base.HBase`
- `f_hs.state.i_0_base.StateBase`
