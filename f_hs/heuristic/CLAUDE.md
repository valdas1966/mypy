# f_hs/heuristic — Heuristic Sources

## Purpose
First-class heuristic objects for AStar (and OMSPP / MOSPP /
MMSPP in later phases). Replaces the raw
`Callable[[State], float]` with an `HBase` hierarchy that also
exposes `is_perfect` (drives early termination) and
`suffix_next` (drives path-stitching on `cache_hit`).

## Package Exports
```python
from f_hs.heuristic import (
    HBase, HCallable, HCached, HBounded, CacheEntry,
)
```

## Architecture
```
HBase[State]  (abstract: __call__, is_perfect=False, suffix_next=None)
  ├── HCallable[State] (wraps Callable; defaults inherited)
  ├── HCached[State]   (frozen dict[State, CacheEntry] + goal;
  │                     perfect-on-hits, delegates to base
  │                     on miss)
  └── HBounded[State]  (frozen dict[State, float] of admissible
                        lower bounds; max-combines with base;
                        is_perfect=False always)
```

## Module Structure
```
heuristic/
├── __init__.py       Lazy __getattr__ aggregator
├── _run_tests.py     f_test.TestRunner entry point
├── i_0_base/         HBase + CacheEntry
├── i_1_callable/     HCallable (AStar callable-wrapper)
├── i_1_cached/       HCached (frozen, goal-keyed)
└── i_1_bounded/      HBounded (frozen bounds; max-combine)
```

## Scope

**Phase 1 (2026-04-20)** — HBase, HCallable, HCached shipped.
Cache static during a search; source: harvested from prior
searches; no bidirectional hooks.

**Phase 2a (2026-04-20)** — HBounded shipped. Bounds static
during a search; admissibility is the caller's responsibility
(not enforced).

**Still deferred** — Felner-style pathmax (Phase 2b) and
bidirectional cache-population hooks (Phase 4).

## Composition
```python
HCached(
    base=HCallable(fn=my_h),
    cache={s1: CacheEntry(h_perfect=..., suffix_next=...), ...},
    goal=my_goal,
)
```
Cache wins where defined; the base callable is consulted
elsewhere.

## Running Tests
```
python -m f_hs.heuristic._run_tests   # HBase + HCallable + HCached
python -m f_hs._run_tests             # full f_hs suite
```
