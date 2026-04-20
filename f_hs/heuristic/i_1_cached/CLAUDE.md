# HCached

## Purpose
Heuristic Source backed by a frozen `dict[State, CacheEntry]`
plus a fallback `HBase`. On a cache hit returns the provably
tight `h_perfect`; on a miss delegates to the base. Powers
AStar's O(1) early-termination when the popped state is in
the cache.

## Static-cache Decision (2026-04-20)
- Cache is **static for the lifetime of this object**. The
  constructor takes a defensive shallow copy; no mutation API.
- Growable caches are deferred until a real use case forces
  them (bidirectional is out of scope for Phase 1).
- Harvested primarily from prior AStar runs via
  `AStar.to_cache()`. External injection for debugging is
  the secondary path.

## Public API

### Constructor
```python
def __init__(self,
             base: HBase[State],
             cache: dict[State, CacheEntry[State]],
             goal: State) -> None
```

### `__call__(state) -> float`
Returns `cache[state].h_perfect` on hit; `self._base(state)` on miss.

### `is_perfect(state) -> bool`
`state in self._cache`.

### `suffix_next(state) -> State | None`
On hit: `cache[state].suffix_next`. On miss: `None`.

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `goal` | `State` | Goal the cache was harvested against |
| `cache` | `dict[State, CacheEntry]` | Read-only shallow copy |

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `graph_abc_full()` | `HCached` | A, B, C all cached; base=0 |
| `graph_abc_partial()` | `HCached` | Only B, C cached; A misses |

## Inheritance
```
HBase[State]
  └── HCached[State]
```

## Tests
`_tester.py` — 7 tests:
1. `test_call_hit_returns_h_perfect` — hit returns cached h.
2. `test_call_miss_delegates_to_base` — miss delegates.
3. `test_is_perfect_only_on_hits` — exact membership semantics.
4. `test_suffix_next_traces_path` — linked-list walk to goal.
5. `test_suffix_next_miss_is_none` — miss returns None.
6. `test_goal_property` — goal exposed.
7. `test_constructor_takes_defensive_copy` — static-cache guard.

## Dependencies
- `f_hs.heuristic.i_0_base.HBase` + `CacheEntry`
- `f_hs.state.i_0_base.StateBase`
