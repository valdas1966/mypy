# AStarLookup

## Purpose

A* enhanced by lookup tables. Accepts optional `cache` and
`bounds` kwargs and builds the heuristic chain internally.
Callers work with plain dicts — `HCached` / `HBounded` /
`HCallable` are framework plumbing, not user API.

In-search Felner pathmax / BPMX(d) lives on `AStarBPMX`
(`i_3_astar_bpmx/`), which extends this class with the
`BPMXMixin` cascade. AStarLookup itself stays focused on the
four lookup-side concerns: HCached early-exit + HBounded
bounds + pre-search `propagate_pathmax` + `to_cache`
harvest.

Lookup semantics:
- `cache: dict[State, CacheEntry]` — perfect `h*(state)` per
  key. Triggers cache-hit early termination and suffix-
  stitched path reconstruction. Requires `goal`.
- `bounds: dict[State, int]` — admissible lower bounds.
  Max-combined with the base heuristic. Unlocks pre-search
  `propagate_pathmax`.

`search_state` is NOT a Pro feature — it lives on `AlgoSPP`
and is available natively on every AStar-family class (simple
AStar, BFS, Dijkstra, AStarLookup, AStarBPMX).

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
  wave-start. Not emitted on `depth=0` or empty seeds.
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

## MRO

```
AStarLookup → AStar → AlgoSPP → Algo → ... → object
```

No BPMXMixin in this MRO — that lives on `AStarBPMX`
(`i_3_astar_bpmx/`).

## Factory
| Method | Description |
|--------|-------------|
| `graph_abc_cached_at_start()` | Cache covering {A,B,C}; 0-expansion early-term |
| `graph_abc_cached_at_b(is_recording)` | Cache covering {B,C}; cache-hit termination at B |
| `grid_4x4()` | Canonical 4x4 grid, no cache, no bounds |

All construct via the kwargs API (`cache=`, `goal=`,
`bounds=`). BPMX-flavoured factories live on
`AStarBPMX.Factory` at `i_3_astar_bpmx/_factory.py`.

## Tests

Auto-discovered by `TestRunner`'s `_tester*.py` pattern.

| File | Scope |
|------|-------|
| `_tester.py` | HCached + HBounded + `propagate_pathmax` lifecycle (3 sections in one file: cached / bounded / pathmax). Includes graph_abc cache-hit counter pins. |
| `_tester_counters.py` | Counter pins on the canonical OOSPP — seven methods: baseline (no cache, no bounds), cached (`(1,1)` at `h*=5`), bounded (`(1,0)` at `h=6`), and four bounded_propagated_depth_{0,1,2,3} (bound `(0,0)=7` + `propagate_pathmax(depth=N)` for `N` in `[0,1,2,3]`). The depth split isolates per-wave deltas: depth-0 ↔ depth-1 = marginal value of wave 0; depth-2 ↔ depth-3 = cost of the no-tighten convergence wave. Drives the param-sensitivity table in `COUNTERS.html`. |
| `_tester_recording.py` | Full event-stream pin scenarios — seven methods mirroring `_tester_counters.py` one-to-one (baseline / cached / bounded / bounded_propagated_depth_{0,1,2,3}). Each asserts every field of every normalized event for the same scenario as the counter-test of the same name. depth-0 has 22 events (no propagate), depth-1 has 24 (1+2+21), depth-2 has 28 (2+5+21), depth-3 has 31 (3+7+21; ≡ depth=None). |

History — `_tester.py` was assembled from three previously
split files (`_tester_cached.py`, `_tester_bounded.py`,
`_tester_pathmax.py`) merged after the BPMX split; the
graph_abc cache-hit counter pins ride along inside it.

BPMX testers live in `i_3_astar_bpmx/`. Dispatch and
seeded-`search_state` testers (which exercise simple `AStar`
/ `AlgoSPP` surface) live in `i_1_astar/_tester_dispatch.py`
and `i_1_astar/_tester_search_state.py`.

Shared `normalize(event)` helper for golden-reference event-
stream comparisons lives at
`f_hs/algo/u_event_normalize.py` (uses `state.event_key()`
polymorphism on `StateBase`).

## Counters

13-name scaffold declared via per-class `_COUNTER_NAMES`.
The constructor replaces `AlgoSPP`'s 8-name scaffold with
this wider one immediately after `AStar.__init__`.

| group | counters | source |
|---|---|---|
| propagate (3) | `cnt_prop_waves`, `cnt_prop_attempts`, `cnt_prop_lifts` | pre-search `propagate_pathmax` |
| frontier (3) | `cnt_push`, `cnt_pop`, `cnt_decrease` | `FrontierPriority` (mirrored on every read) |
| search (2) | `cnt_expanded`, `cnt_generated` | inherited from AlgoSPP |
| memory (5) | `mem_open`, `mem_closed`, `mem_cache`, `mem_bounds`, `mem_total` | post-run `_memory_snapshot()`; `mem_total = Σ mem_*` finalized last via `u_mem.finalize_mem_total` |

**Counter semantics** — `cnt_prop_*` (set inside
`propagate_pathmax`):
- `cnt_prop_waves` — number of waves run; equals count of
  `propagate_wave` events.
- `cnt_prop_attempts` — total `(source, child)` propagate
  attempts; equals count of `propagate` events. Excludes
  back-edge / cached-target short-circuits.
- `cnt_prop_lifts` — successful tightenings (subset of
  attempts where `was_improved=True`).

All stay 0 if `propagate_pathmax()` is never called.

**Pre-search retention.** `propagate_pathmax` runs BEFORE
`run()`, but the counters it sets must persist into the
post-`run()` snapshot — otherwise calling propagate then run
silently wipes the propagate accounting. AStarLookup declares
`_PRESEARCH_COUNTER_NAMES = ('cnt_prop_waves',
'cnt_prop_attempts', 'cnt_prop_lifts')`; `AlgoSPP._init_search`
preserves listed counters across its `_counters.reset()`,
mirroring the recorder's retention of pre-search `propagate` /
`propagate_wave` events.

`AStarBPMX` overrides `_COUNTER_NAMES` to a 15-name shape by
prepending the `cnt_bpmx_*` group.

## Inheritance

```
AlgoSPP[State]
    └── AStar[State]                   (simple)
        └── AStarLookup[State]         (this class)
            └── AStarBPMX[State]       (i_3_astar_bpmx/)
```

## Dependencies
- `f_hs.algo.i_1_astar.AStar` (base)
- `f_hs.algo.i_0_base.AlgoSPP` (via AStar)
- `f_core.counters.Counters` (scaffold replacement)
- `f_hs.heuristic.i_0_base.HBase` + `CacheEntry`
- `f_hs.heuristic.i_1_cached.HCached`
- `f_hs.heuristic.i_1_bounded.HBounded`
- `f_hs.heuristic.i_1_callable.HCallable`
