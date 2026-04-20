# AStar

## Purpose
A* Search Algorithm using `FrontierPriority` (backed by
`QueueIndexed` — indexed min-heap with decrease_key). Matches
classical textbook pseudocode — eager deletion, each state
appears at most once in FRONTIER.

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
             h: HBase[State] | Callable[[State], float],
             name: str = 'AStar',
             is_recording: bool = False,
             search_state: SearchStateSPP[State] | None = None
             ) -> None
```
Injects `FrontierPriority[State]()` into `AlgoSPP`. Accepts
either an `HBase` subclass or a raw `Callable` — callables are
auto-wrapped in `HCallable`, so existing call sites that pass a
lambda keep working unchanged.

**Admissibility guard.** If `h` is an `HCached`, its `goal`
must be in `problem.goals` — otherwise `__init__` raises
`ValueError`. A cache harvested against the wrong goal silently
violates A*'s admissibility (cached h* to the wrong goal may
over-estimate h* to the right one).

**`search_state` kwarg** — pre-built bundle injection (see
`AlgoSPP/CLAUDE.md`). Use `resume()` to pump from the seeded
state. Push into the caller's frontier with
`seed.frontier.push(state, priority=algo._priority(state))`
after construction; the recorder then captures only
post-resume events.

**Heuristic variants** — the `h` parameter accepts any `HBase`
subclass: `HCallable` (wraps a function), `HCached` (perfect-h
+ suffix), or `HBounded` (admissible lower bounds,
max-combined with a base). For `HBounded`, no special handling:
`_priority` reads `self._h(state)` which auto-routes through
the max-combine; `is_perfect=False` keeps `cache_rank=1` and
the goal-mismatch guard does not fire (HBounded carries no
goal).

### Pre-Search Pathmax Propagation
```python
def propagate_pathmax(self, depth: int = 2) -> dict[State, float]
```
Felner-style forward pathmax applied as a **setup step** (pre-
`run()` / pre-`resume()`). Walks `depth` waves from cached /
bounded seeds, inserting `max(h(n), h(s) - w(s, n))` at each
non-cached neighbor via `HBounded.add_bound`. Returns a
cumulative `dict[State, float]` of every state whose bound
was tightened, mapped to its final post-propagation h.

**Requirements** — `self._h` is `HBounded`, or wraps one via
the `_base` chain (e.g., `HCached(base=HBounded(...), ...)`).
Otherwise raises `ValueError`.

**Semantics**:
- Wave 0 seeds = cached state keys UNION bounded state keys.
- Wave `k >= 1` sources = states strictly tightened in wave `k-1`.
- Targets EXCLUDE cached states (cache is tighter-or-equal).
- `depth=0` is a valid no-op. `depth<0` raises.
- Terminates early when a wave tightens nothing.
- No recorder events emitted — pathmax is setup, not a search
  step (mirrors `refresh_priorities`).

**Admissibility** preserved: `h(s) ≤ h*(s)` + inequality
`h*(n) ≥ h*(s) - w(s, n)` ⇒ `h(s) - w(s, n)` is an admissible
lower bound on `h*(n)`.

Phase 2b deliverable; in-search BPMX (backward pathmax during
expansion) is deferred to Phase 2c.

**Recording.** When `is_recording=True`, each strict tightening
emits a `propagate` event:
```
{type: 'propagate', state: child, parent: source,
 h_parent: h_source_at_propagation, h: new_h_child}
```
No `g` / `f` — pre-search, not applicable. No `is_bounded`
flag on the event (the subsequent push/pop of the state
carries it). Emission is deterministic: sources are iterated
in `sorted(...)` order each wave, so recording tests are
stable across Python runs. `w` is derivable as
`h_parent - h` (strict tightening); not recorded.

### Cache Harvest
```python
def to_cache(self) -> dict[State, CacheEntry[State]]
```
Emit on-path cache entries from the last completed run.
Supports **both** termination modes:
- **Goal-pop** (`search_state.goal_reached` set): walks
  start → goal, `total_cost = g(goal)`.
- **Cache-hit** (`search_state.cache_hit` set): walks
  start → cache_hit, `total_cost = g(cache_hit) +
  h_perfect(cache_hit)`. The terminal entry's `suffix_next`
  points into the existing cache (so chaining onto the prior
  cache preserves the suffix).

For each on-path state `s`:
```
h_perfect[s]  = total_cost - g(s)
suffix_next   = next state on the walked chain (or the cache's
                own suffix_next for the terminal in cache-hit mode;
                None for the goal in goal-pop mode)
```
Raises `ValueError` if neither termination mode fired
(frontier exhausted — no solution).

This is the mechanism that makes OMSPP / MOSPP / MMSPP
incremental-reuse possible: each query emits a harvest that
extends the cache fed to the next query. (2026-04-20 locked
use case.)

### Path Reconstruction
`reconstruct_path(goal=None)` — when termination was via
`cache_hit` and no explicit `goal` was passed, walks parents
to `cache_hit` and stitches the cached suffix via
`HCached.suffix_next`. Passing `goal` explicitly bypasses the
stitching.

## Priority / Tie-Breaking
```python
def _priority(self, state: State) -> tuple:
    g = self._search.g[state]
    f = g + self._h(state)
    cache_rank = 0 if self._h.is_perfect(state) else 1
    return (f, -g, cache_rank, state)
```
Four-level priority, compared lexicographically by the min-heap:
- **f = g + h** (primary): total estimated cost.
- **-g** (secondary): prefer deeper nodes (closer to goal).
- **cache_rank** (tertiary): cached (0) before uncached (1).
  A cached pop gives O(1) early-termination — strictly less
  work than expanding an uncached tie. Optimality is unaffected
  (tie-breaks after `f` don't touch admissibility).
- **state** (quaternary): fall back to State's `Comparable`
  ordering (via `HasKey`). Deterministic, independent of
  heap-internal ordering — required for full-sequence recording
  tests where `(f, -g, cache_rank)` ties are common.

For non-HCached heuristics `is_perfect` is always False, so
`cache_rank` is a constant 1; the tuple effectively collapses
to `(f, -g, 1, state)` — behaviourally identical to the pre-cache
`(f, -g, state)` ordering (no existing-test drift).

## Event Enrichment
AStar overrides `_enrich_event` to add:
- `h` and `f` on `push`, `pop`, `decrease_g` events — `f` is
  `event['g'] + h(state)`, not the priority tuple.
- `is_cached=True` on `push` and `pop` events whose state has a
  perfect heuristic (`self._h.is_perfect(state)`).
- `is_bounded=True` on `push` and `pop` events whose state has
  a strictly-tightening bound (`self._h.is_bounded(state)`,
  i.e., `HBounded`'s bound > base for that state).

Both flags are **absent** (not False) when not applicable —
the framework Recording Principle forbids constant-False flags.
`decrease_g` does NOT carry either flag: cache / bound
membership was already signalled on the state's initial push.

No dedicated cache-hit event type. The cache-hit terminator is
identifiable as "the last pop carrying `is_cached=True`" —
mirroring goal-pop termination (also implicit, no
`goal_reached` event). `is_bounded` has no terminator
semantics — it's purely visibility into which states benefited
from the bound.

## Early-Exit Override
AStar overrides `_early_exit(state)`:
```python
if self._h.is_perfect(state):
    self._search.cache_hit = state
    return SolutionSPP(cost=g(state) + h_perfect(state))
return None
```
No event is emitted — the pop recorded just before this hook
already carries `is_cached=True` via `_enrich_event`. Only
`HCached` returns True from `is_perfect`, so `HCallable`-backed
AStar keeps classical behavior.

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `graph_abc()` | `AStar` | Linear graph, admissible h |
| `graph_no_path()` | `AStar` | No path, h=0 |
| `graph_start_is_goal()` | `AStar` | Start == Goal, h=0 |
| `graph_diamond()` | `AStar` | Diamond graph, admissible h |
| `grid_3x3()` | `AStar` | Open grid, Manhattan h |
| `grid_3x3_obstacle()` | `AStar` | Grid with obstacle |
| `grid_3x3_no_path()` | `AStar` | Grid with wall |
| `grid_3x3_start_is_goal()` | `AStar` | Grid where start == goal |
| `grid_4x4_obstacle()` | `AStar` | 4x4 grid with vertical wall, cost 7 |
| `graph_decrease()` | `AStar` | Weighted graph (S→A/B→X, w(B,X)=0), h=0 — forces `decrease_g` and exercises h/f enrichment on it |
| `graph_abc_cached_at_start()` | `AStar` | HCached covering {A,B,C}; degenerate cache_hit on pop(A) |
| `graph_abc_cached_at_b()` | `AStar` | HCached covering {B,C}; non-degenerate cache_hit on pop(B), drives the `to_cache()`-after-cache_hit harvest test |

## Inheritance
```
AlgoSPP[State]
    └── AStar[State]
        └── Dijkstra[State]
```

## Tests
Split into three files by concern (mirrors the BFS split).
No `@pytest.fixture` — each test calls `AStar.Factory.*`
directly, per the Factory-over-fixture rule.

| File | Scope | Count |
|------|-------|-------|
| `_tester.py` | Graph problems + lifecycle (incl. `search_state`, `resume`, `cache_hit` early-term, `to_cache` round-trip, `to_cache` after cache_hit, goal-mismatch guard) | 11 |
| `_tester_grid.py` | Grid problems | 4 |
| `_tester_recording.py` | Full event-sequence assertion (incl. `decrease_g` + h/f enrichment, the `cache_hit` event schema, and seeded-resume recording via the `search_state` kwarg) | 8 |

Run all three explicitly:
```
pytest f_hs/algo/i_1_astar/_tester.py \
       f_hs/algo/i_1_astar/_tester_grid.py \
       f_hs/algo/i_1_astar/_tester_recording.py
```

The recording tester covers `graph_abc`, `graph_diamond`
(tie-break via State Comparable), `grid_3x3`, `grid_3x3_obstacle`,
and `grid_4x4_obstacle` (same problem used by BFS, exercising
an admissible-but-loose Manhattan heuristic over a wall).

## Dependencies
- `f_hs.algo.i_0_base.AlgoSPP`
- `f_hs.frontier.i_1_priority.FrontierPriority`
- `f_hs.heuristic.i_0_base.HBase` + `CacheEntry`
- `f_hs.heuristic.i_1_callable.HCallable`
- `f_hs.heuristic.i_1_cached.HCached`
