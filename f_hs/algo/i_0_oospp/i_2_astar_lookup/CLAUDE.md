# AStarLookup

## Purpose

A* enhanced by lookup tables. Accepts optional `cache` and
`bounds` dicts as kwargs and builds the heuristic chain
internally. Callers work with plain dicts — `HCached` /
`HBounded` / `HCallable` are framework plumbing, not user API.

Lookup semantics:
- `cache: dict[State, CacheEntry]` — perfect `h*(state)` per
  key. Triggers cache-hit early termination and suffix-
  stitched path reconstruction. Requires `goal`.
- `bounds: dict[State, int]` — admissible lower bounds.
  Max-combined with the base heuristic. Unlocks pre-search
  `propagate_pathmax`.

`search_state` is NOT a Pro feature — it lives on `AlgoSPP`
and is available natively on every AStar-family class (simple
AStar, BFS, Dijkstra, AStarLookup).

In-search BPMX is **not** a feature of `AStarLookup`. The
Felner pathmax rules and the BPMX(d) cascade live on the
sibling class `AStarBPMX` (`f_hs/algo/i_2_astar_bpmx/`) and
on the integrated class `AStarLookupBPMX`
(`f_hs/algo/i_3_astar_lookup_bpmx/`) which composes the
shared `BPMXMixin` with this class for cache + bounds +
in-search BPMX in one pass (used by k×A*-CB for OMSPP /
MOSPP sub-search reuse).

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
             h: HBase[State] | Callable[[State], int] | None = None,
             name: str = 'AStar',
             is_recording: bool = False,
             search_state: SearchStateSPP[State] | None = None,
             cache: dict[State, CacheEntry[State]] | None = None,
             goal: State | None = None,
             bounds: dict[State, int] | None = None,
             ) -> None
```

Three ways to supply the heuristic:
1. **Base callable + dicts** (the documented path): pass
   `h=my_callable`, plus `cache=...` and/or `bounds=...`. The
   class assembles `HCached(base=HBounded(base=HCallable(h)))`
   internally, wrapping only the layers requested.
2. **Pre-built HBase** (escape hatch): pass `h=HCached(...)` or
   similar; `cache`/`bounds` must then be None (refused,
   ValueError). Useful when sharing a constructed heuristic
   across multiple queries.
3. **No heuristic at all**: omit `h`; internally uses
   `lambda s: 0`, effectively Dijkstra-flavoured Lookup.

**Validation**:
- `cache` without `goal` → `ValueError`.
- Pre-built HBase `h` combined with `cache` or `bounds` →
  `ValueError` (would double-wrap).
- HCached goal not in `problem.goals` → `ValueError`
  (A* admissibility).

### Pre-Search Pathmax Propagation
```python
def propagate_pathmax(self,
                      depth: int | None = None
                      ) -> dict[State, float]
```
Walks pathmax waves from cached / bounded seeds.

`depth`:
- `None` (default) — **run to convergence**. Stops when a wave
  tightens nothing; natural termination. Bounded above by the
  graph's pathmax-reachable diameter.
- `int >= 0` — cap at that many waves.
- `int < 0` — raises `ValueError`.

Optimisations:
- Cached targets skipped (cache is perfect; any propagated
  lower bound is ≤ cached h).
- Last-tightener back-edge skipped (provably useless under
  positive-weight SPP).

Recording:
- **`propagate_wave`** — emitted at the start of each wave
  that runs. Fields: `{type: 'propagate_wave', depth: int,
  num_sources: int}`. State-less meta-event — marks the
  boundary so consumers can group `propagate` events by wave
  without counting. `num_sources` is `len(sources)` at
  wave-start — the count of source states about to propagate.
  Not emitted on `depth=0` or empty seeds.
- **`propagate`** — every (source, child) attempt (except
  skipped back-edges). Fields: `{type, state, parent,
  h_parent, h, was_improved: bool}`.

Returns `dict[State, float]` of tightened states mapped to
their final h values.

### Cache Harvest
```python
def to_cache(self) -> dict[State, CacheEntry[State]]
```
Harvest on-path cache entries from the last completed run.
Supports both goal-pop and cache-hit termination. Emits
`CacheEntry(h_perfect, suffix_next)` for each on-path state.

### Path Reconstruction
`reconstruct_path(goal=None)` — on cache-hit termination with
no explicit `goal`, stitches the cached suffix via
`HCached.suffix_next`.

## Priority / Tie-Breaking
```python
(f, -g, cache_rank, state)
```
`cache_rank = 0` when `is_perfect(state)`, else `1`. Four-level
lexicographic order; behaviourally equivalent to simple A*'s
3-tuple when no states are cached (cache_rank constant 1).

## Event Enrichment
Extends AStar's h/f with:
- `is_cached=True` on push / pop when perfect-h hit.
- `is_bounded=True` on push / pop when strictly bounded beyond
  base (state property).
- `int()` cast of `h` / `h_parent` on propagate events.

Both flags absent (not False) on non-applicable events.
`was_improved` on propagate events is an event-outcome flag
(see Pre-Search Pathmax Propagation section).

## Factory
| Method | Description |
|--------|-------------|
| `graph_abc_cached_at_start()` | Cache covering {A,B,C}; 0-expansion early-term |
| `graph_abc_cached_at_b()` | Cache covering {B,C}; non-degenerate cache-hit |

Both construct via the new kwargs API (`cache=`, `goal=`) —
demonstrates the documented path.

## Tests

Split by feature into five files; auto-discovered by
`TestRunner`'s `_tester*.py` pattern.

| File | Scope | Count |
|------|-------|-------|
| `_tester_dispatch.py` | Simple-AStar rejection of HCached/HBounded; simple AStar accepts search_state | 3 |
| `_tester_cached.py` | HCached lifecycle + recording | 7 |
| `_tester_bounded.py` | HBounded lifecycle + recording | 3 |
| `_tester_pathmax.py` | `propagate_pathmax` (depth None / 0 / int, convergence, multi-wave) | 7 |
| `_tester_search_state.py` | Seeded resume lifecycle + recording | 3 |

23 tests total. Shared `normalize(event)` helper for golden-
reference event-stream comparisons lives at
`f_hs/algo/u_event_normalize.py` (uses `state.event_key()`
polymorphism on `StateBase`). In-search BPMX tests live on
`AStarBPMX` (`f_hs/algo/i_0_oospp/i_2_astar_bpmx/_tester*.py`).

## Counters

AStarLookup extends the inherited frontier-mirror scaffold
with a `propagate` group that tracks the pre-search
`propagate_pathmax` work.

| group | counters |
|---|---|
| propagate (3) | `cnt_prop_waves`, `cnt_prop_attempts`, `cnt_prop_lifts` |
| frontier (3) | `cnt_push`, `cnt_pop`, `cnt_decrease` (mirrored from `FrontierPriority`) |
| memory (4) | `mem_open`, `mem_closed`, `mem_cache`, `mem_bounds` (post-run snapshot) |

**`cnt_prop_*` semantics** (set inside `propagate_pathmax`):

- `cnt_prop_waves` — number of waves run (capped by `depth`;
  natural termination on no-improvement). Equals the count of
  `propagate_wave` events.
- `cnt_prop_attempts` — total `(source, child)` propagate
  attempts. Equals the count of `propagate` events. Excludes
  back-edge / cached-target short-circuits.
- `cnt_prop_lifts` — successful tightenings (subset of
  attempts where `was_improved=True` on the propagate event).

All three stay 0 if `propagate_pathmax()` is never called.
Frontier counters are sourced from `FrontierPriority` on every
read.

## Inheritance

```
AlgoSPP[State]
    └── AStar[State]                   (simple)
        └── AStarLookup[State]         (this class)
```

## Dependencies
- `f_hs.algo.i_1_astar.AStar` (base)
- `f_hs.algo.i_0_base.AlgoSPP` (via AStar)
- `f_hs.heuristic.i_0_base.HBase` + `CacheEntry`
- `f_hs.heuristic.i_1_cached.HCached`
- `f_hs.heuristic.i_1_bounded.HBounded`
- `f_hs.heuristic.i_1_callable.HCallable`
