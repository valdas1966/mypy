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
  Max-combined with the base heuristic. Unlocks
  `propagate_pathmax`.

`search_state` is NOT a Pro feature — it lives on `AlgoSPP`
and is available natively on every AStar-family class (simple
AStar, BFS, Dijkstra, AStarLookup).

## Public API

### In-Search BPMX (`bpmx` kwarg)

```python
AStarLookup(..., bpmx: str | None = None)
```

Enables in-search bidirectional pathmax (Felner et al. 2011)
for inconsistent heuristics. The HCached ∘ HBounded ∘ HCallable
chain is intrinsically inconsistent at the cache boundary;
BPMX propagates tightening during the search, complementing
pre-search `propagate_pathmax`.

Valid values: `None` (off, default), `'1'`, `'2'`, `'12'`,
`'23'`, `'123'`. Rejected: `'3'`, `'13'` (Rule 3 cascade
requires Rule 2 as trigger).

Rule semantics (MOSPP report numbering):
- **Rule 1**: forward pathmax — `h(c) ← max(h(c), h(n) − w(n,c))`
  at parent expansion. Child's h lifted from parent.
- **Rule 2**: backward pathmax — `h(n) ← max(h(n), max_c(h(c) − w(c,n)))`
  at parent expansion. Parent's h lifted from children.
- **Rule 3**: cascade — iterate Rules 1 and 2 until fixed point.

Auto-wrap: when `bpmx` is set and no explicit `bounds` supplied,
an empty `HBounded` is auto-wrapped into the chain as storage
for lifted h values. Pre-built HBase `h` without HBounded in
its chain → `ValueError`.

Static-bounds invariant: BPMX mutates `HBounded._bounds`
during search (calls `add_bound`). Deliberate relaxation of
the 2026-04-20 "bounds static during search" decision, scoped
to the BPMX code path. Documented in the HBounded CLAUDE.md.

Recording: `bpmx_lift` event on Rule 2 fires;
`bpmx_forward` on Rule 1. Schema:
- `{type: 'bpmx_lift', state=n, h_old, h_new, via_child}`.
- `{type: 'bpmx_forward', state=c, h_old, h_new, via_parent}`.

Frontier staleness: Rule 1 can tighten a child's h after that
child has been pushed from an earlier path; the heap keeps
old priority. A* with inconsistent h accepts this (Martelli);
paper Algorithm 2 makes the same pragmatic choice.

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
| `_tester_bpmx.py` | `bpmx` kwarg: validation, rule mechanics, admissibility, A/B vs propagate_pathmax | 13 |

23 tests total. Shared helpers (`key_of`, `normalize`) in
`_utils.py`.

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
