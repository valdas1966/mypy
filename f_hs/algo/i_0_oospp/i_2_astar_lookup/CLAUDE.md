# AStarLookup

## Purpose

A* enhanced by lookup tables and (optional) in-search Felner
pathmax / BPMX(d). Accepts optional `cache`, `bounds`,
`rule_bpmx`, `depth_bpmx` kwargs and builds the heuristic
chain internally. Callers work with plain dicts — `HCached`
/ `HBounded` / `HCallable` are framework plumbing, not user
API.

The canonical advanced-A* class. Composes `BPMXMixin`
natively (Phase-1 merge, 2026-05-06): cache + bounds +
pre-search `propagate_pathmax` + (optional) in-search
BPMX(d) live on this single class. Used by k×A*-CB for
OMSPP / MOSPP sub-search.

Lookup semantics:
- `cache: dict[State, CacheEntry]` — perfect `h*(state)` per
  key. Triggers cache-hit early termination and suffix-
  stitched path reconstruction. Requires `goal`.
- `bounds: dict[State, int]` — admissible lower bounds.
  Max-combined with the base heuristic. Unlocks pre-search
  `propagate_pathmax`.

BPMX semantics (composed via `BPMXMixin`):
- `rule_bpmx ∈ {None, '1', '2', '3', 'CASCADE'}` — selects
  which Felner rule (or cascade) runs at each `_pre_expand`.
  `None` (default) ⇒ mechanism off.
- `depth_bpmx ∈ {None, int >= 1}` — BFS-subtree depth for
  Rules 1 / 3 / CASCADE; Rule 2 is depth-1 only by
  structural constraint.

`search_state` is NOT a Pro feature — it lives on `AlgoSPP`
and is available natively on every AStar-family class (simple
AStar, BFS, Dijkstra, AStarLookup).

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
             rule_bpmx: str | None = None,
             depth_bpmx: int | None = 1,
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

**BPMX storage auto-wrap:** when `rule_bpmx is not None` AND
`h` is a callable / None AND `bounds` is None, the
constructor synthesizes an empty `bounds={}` so the chain
builder includes the HBounded layer needed as storage for
lifted h-values. With a pre-built HBase chain, the host
must supply HBounded (constructor verifies; ValueError
otherwise).

**Validation**:
- `rule_bpmx not in {None, '1', '2', '3', 'CASCADE'}` →
  `ValueError`.
- `depth_bpmx not in {None} ∪ {int >= 1}` → `ValueError`.
- `rule_bpmx == '2'` with `depth_bpmx != 1` → `ValueError`
  (Rule 2 cannot propagate beyond depth 1).
- `cache` without `goal` → `ValueError`.
- Pre-built HBase `h` combined with `cache` or `bounds` →
  `ValueError` (would double-wrap).
- HCached goal not in `problem.goals` → `ValueError`
  (A* admissibility).
- BPMX enabled but no HBounded reachable → `ValueError`.

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

### In-search BPMX (BPMXMixin)

When `rule_bpmx is not None`, every non-cached pop runs
`_pre_expand` → `BPMXMixin._apply_bpmx`, dispatching to:

- `'1'` — Rule 1 (Mero, 1984), parent → child top-down sweep,
  `depth_bpmx` levels.
- `'2'` — Rule 2 (Felner), children → parent via min, depth-1.
- `'3'` — Rule 3 (Felner), strongest child → parent bottom-up,
  `depth_bpmx` levels.
- `'CASCADE'` — Felner Algorithm 2 (Rules 1 + 3 alternating,
  iterated to fixed point over the d-level subtree).

A cached state in the cascade subtree is skipped from lift
mutation (`is_perfect` guard). Cache-hit early-exit fires
BEFORE `_pre_expand`, so a cached pop never runs the
cascade.

Recording event types added by the mixin:
- `pathmax_apply{rule=2}`, `bpmx_lift`, `bpmx_forward`,
  `bpmx_iteration` (CASCADE only).

See `mixins/bpmx/CLAUDE.md` for full mechanism details.

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
- BPMXMixin int-casts on `pathmax_apply` / `bpmx_lift` /
  `bpmx_forward` (chained via `super()`).

Both flags absent (not False) on non-applicable events.
`was_improved` on propagate events is an event-outcome flag
(see Pre-Search Pathmax Propagation section).

## MRO

```
AStarLookup → BPMXMixin → AStar → AlgoSPP → Algo → ... → object
```

`BPMXMixin` sits between `AStarLookup` and `AStar` so the
mixin's `_pre_expand` / `counters` / `_enrich_event`
overrides resolve before the simple-A* fallback. The
`_enrich_event` chain runs in MRO order: `AStarLookup`
calls `super()._enrich_event(event)` first → BPMXMixin int-
casts → AStar h/f; then this class layers `is_cached` /
`is_bounded` / propagate casts on top.

## Factory
| Method | Description |
|--------|-------------|
| `graph_abc_cached_at_start()` | Cache covering {A,B,C}; 0-expansion early-term |
| `graph_abc_cached_at_b(rule_bpmx, depth_bpmx, is_recording)` | Parametric — cache covering {B,C}; defaults reproduce off-mode |
| `grid_4x4(rule_bpmx, depth_bpmx)` | Parametric — canonical 4x4 grid, no cache; defaults reproduce plain AStar |
| `graph_diamond_inconsistent_cascade()` | Inconsistent diamond + CASCADE(∞), recording on |
| `grid_4x4_cached_suffix_cascade_d1()` | Goal-cached + CASCADE depth=1 |

All construct via the kwargs API
(`cache=`, `goal=`, `bounds=`, `rule_bpmx=`, `depth_bpmx=`).

## Tests

Split by feature; auto-discovered by `TestRunner`'s
`_tester*.py` pattern.

| File | Scope |
|------|-------|
| `_tester_dispatch.py` | Simple-AStar rejection of HCached/HBounded; simple AStar accepts search_state |
| `_tester_cached.py` | HCached lifecycle + recording |
| `_tester_bounded.py` | HBounded lifecycle + recording |
| `_tester_pathmax.py` | `propagate_pathmax` (depth None / 0 / int, convergence, multi-wave) |
| `_tester_search_state.py` | Seeded resume lifecycle + recording |
| `_tester_counters.py` | Counter scaffold pin (no cache, no bounds, no BPMX) |
| `_tester_recording.py` | Full event-stream pin scenarios |
| `_tester_bpmx_with_cache.py` | Cache + BPMX integration (validation, optimality, MRO) |
| `_tester_bpmx_no_cache.py` | BPMX without cache (validation, optimality, lift events on inconsistent diamond, generic schema) |
| `_tester_counters_bpmx_with_cache.py` | Cache + BPMX counter scenarios |
| `_tester_counters_bpmx_no_cache.py` | Per-rule counter pins on grid_4x4_obstacle (no cache) |
| `_tester_recording_bpmx_with_cache.py` | Cache + BPMX recording scenarios |
| `_tester_recording_bpmx_no_cache.py` | Per-rule full event-stream pins on grid_4x4_obstacle (no cache) |

Shared `normalize(event)` helper for golden-reference event-
stream comparisons lives at
`f_hs/algo/u_event_normalize.py` (uses `state.event_key()`
polymorphism on `StateBase`). The `_tester_*_bpmx_*.py`
files cover all BPMX scenarios (standalone with no cache,
combined with cache, and edge cases).

## Counters

15-name scaffold declared via `_COUNTER_NAMES` (per-class
override of `BPMXMixin._BPMX_COUNTER_NAMES`).

| group | counters | source |
|---|---|---|
| propagate (3) | `cnt_prop_waves`, `cnt_prop_attempts`, `cnt_prop_lifts` | pre-search `propagate_pathmax` |
| bpmx (3) | `cnt_bpmx_attempts`, `cnt_bpmx_successes`, `cnt_bpmx_depth` | in-search BPMX dispatch |
| frontier (3) | `cnt_push`, `cnt_pop`, `cnt_decrease` | `FrontierPriority` (mirrored on every read) |
| search (2) | `cnt_expanded`, `cnt_generated` | inherited from AlgoSPP |
| memory (4) | `mem_open`, `mem_closed`, `mem_cache`, `mem_bounds` | post-run `_memory_snapshot()` |

**Counter semantics**:

- `cnt_prop_*` (set inside `propagate_pathmax`):
  - `cnt_prop_waves` — number of waves run; equals count of
    `propagate_wave` events.
  - `cnt_prop_attempts` — total `(source, child)` propagate
    attempts; equals count of `propagate` events. Excludes
    back-edge / cached-target short-circuits.
  - `cnt_prop_lifts` — successful tightenings (subset of
    attempts where `was_improved=True`).
  All stay 0 if `propagate_pathmax()` is never called.
- `cnt_bpmx_*` (set inside `_pre_expand` / sweep functions):
  - `cnt_bpmx_attempts` — incremented once per `_pre_expand`
    call when `rule_bpmx is not None`. Cumulative.
  - `cnt_bpmx_successes` — per-lift count, regardless of rule.
    Cumulative.
  - `cnt_bpmx_depth` — max-tracker (deepest BFS-level at
    which any lift fired).
  All stay 0 in off-mode (`rule_bpmx=None`).

Cache-hit interaction: when a cached state is popped,
`_early_exit` fires BEFORE `_pre_expand`, so the cascade
does NOT run for that pop. `cnt_bpmx_attempts` therefore
can be strictly less than the count of non-goal pops when
the cache covers any expansion target.

## Inheritance

```
AlgoSPP[State]
    └── AStar[State]                   (simple)
        └── AStarLookup[State]         (this class — composes
                                       BPMXMixin natively)
```

## Dependencies
- `f_hs.algo.i_1_astar.AStar` (base)
- `f_hs.algo.i_0_base.AlgoSPP` (via AStar)
- `f_hs.algo.i_0_oospp.mixins.bpmx.BPMXMixin` (composed)
- `f_hs.heuristic.i_0_base.HBase` + `CacheEntry`
- `f_hs.heuristic.i_1_cached.HCached`
- `f_hs.heuristic.i_1_bounded.HBounded`
- `f_hs.heuristic.i_1_callable.HCallable`
