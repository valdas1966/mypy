# HBase

## Purpose
Abstract base class for heuristic sources consumed by AStar.
Decouples AStar from raw `Callable[[State], float]` so that
richer heuristics (cached perfect-h, bounded h, pathmax-aware h)
can plug in without touching AStar's loop.

## Public API

### `__call__(state) -> float`
Return h(state). Base raises `NotImplementedError` — subclasses
(`HCallable`, `HCached`) override.

### `is_perfect(state) -> bool`
Default `False`. `HCached` overrides to True on cached states;
AStar uses this to decide early termination on the popped state.

### `suffix_next(state) -> State | None`
Default `None`. `HCached` overrides to return the next state on
the cached optimal suffix (linked-list style); AStar uses this
to stitch the suffix onto a `cache_hit`-terminated path.

### `is_bounded(state) -> bool`
Default `False`. `HBounded` overrides to return True iff its
bound at `state` is strictly greater than the base h at `state`
— i.e., the bound tightened h. AStar enriches `push` / `pop`
events with `is_bounded=True` when this returns True; absent
otherwise (Recording Principle — no constant-False flags).

## CacheEntry
`@dataclass(frozen=True)` in `_cache_entry.py`. Two fields:
| Field | Type | Meaning |
|-------|------|---------|
| `h_perfect` | `float` | h*(state → goal) |
| `suffix_next` | `State | None` | next on optimal suffix, or None for the goal |

Frozen — cache is static during an AStar run (2026-04-20 decision).

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `base()` | `HBase[StateBase[str]]` | Defaults test subject |
| `entry_goal()` | `CacheEntry` | `(0.0, None)` — a goal cell |
| `entry_pre_goal()` | `CacheEntry` | `(1.0, StateBase('C'))` |

## Inheritance
```
HBase[State]
  ├── HCallable[State]    (i_1_callable)
  └── HCached[State]      (i_1_cached)
```

## Tests
`_tester.py` — 4 tests:
1. `test_call_raises` — default __call__ raises.
2. `test_is_perfect_default_false` — default.
3. `test_suffix_next_default_none` — default.
4. `test_cache_entry_frozen` — frozen dataclass.

## Dependencies
- `f_hs.state.i_0_base.StateBase`
