# AStar

## Purpose

A* Search Algorithm — simple, fast path. Canonical A* with
priority `(f, −g, state)` and minimal event enrichment.
Accepts any `HBase` / raw callable EXCEPT `HCached` /
`HBounded`, which route to `AStarLookup` (raises `TypeError`
with a redirecting message — silent acceptance would be a
correctness trap).

`search_state` is supported natively — lives on `AlgoSPP` as
a generic capability (seeded resume, auto-refresh of stale
frontier priorities). Available on every AStar-family class.

For advanced workflows (HCached, HBounded, pathmax
propagation), see `AStarLookup` at `i_2_astar_lookup/`. It
takes `cache` and `bounds` dicts directly as kwargs — callers
don't interact with HCached / HBounded classes.

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
Injects `FrontierPriority[State]()` into `AlgoSPP`. Callables
are auto-wrapped in `HCallable`. The `search_state` kwarg is
accepted for kwarg-flow compatibility with the `__new__`
dispatcher and for Dijkstra's forwarding; on a simple AStar
instance it is always None (a non-None value routes to
`AStarLookup`).

### HCached / HBounded rejection
`AStar.__init__` raises `TypeError` when a direct instantiation
(not via subclass) receives an HCached or HBounded `h`. Rationale:
- No early exit → user loses cache-hit termination silently.
- No suffix stitch → `reconstruct_path` gives wrong paths on
  cache hits.
- No admissibility guard → bad-goal HCached produces wrong
  answers.

The rejection is gated on `type(self) is AStar` so subclasses
(AStarLookup) can still call `AStar.__init__` internally with
assembled HCached/HBounded chains.

## Priority / Tie-Breaking
```python
def _priority(self, state: State) -> tuple:
    g = self._search.g[state]
    f = g + self._h(state)
    return (f, -g, state)
```
Three-level lexicographic:
1. **f** — lower first.
2. **−g** — deeper first.
3. **state** — deterministic tiebreak via HasKey Comparable.

No `cache_rank` at this level — the 4-tuple with cache_rank
lives on `AStarLookup._priority`.

## Event Enrichment
```python
def _enrich_event(self, event: dict) -> None:
    t = event.get('type')
    if t in ('push', 'pop', 'decrease_g'):
        h = self._h(event['state'])
        f = event['g'] + h
        event['h'] = self._as_int_if_whole(h)
        event['f'] = self._as_int_if_whole(f)
```
Only `h` and `f`, cast to int when integer-valued. No
`is_cached` / `is_bounded` flags — those are AStarLookup's
responsibility. No propagate-event handling either (propagate
is a Pro-only event).

## Factory
| Method | Description |
|--------|-------------|
| `graph_abc()` | Linear A -> B -> C, admissible h |
| `graph_no_path()` | No path, h=0 |
| `graph_start_is_goal()` | Start == Goal, h=0 |
| `graph_diamond()` | Diamond graph, admissible h |
| `graph_decrease()` | Weighted graph (w(B,X)=0), h=0 — exercises `decrease_g` + h/f enrichment |
| `grid_3x3()` | Open grid, Manhattan h |
| `grid_3x3_obstacle()` | Grid with obstacle |
| `grid_3x3_no_path()` | Grid with wall |
| `grid_3x3_start_is_goal()` | Start == Goal |
| `grid_4x4_obstacle()` | 4x4 grid, vertical wall, cost 7 |

All simple-h factories. HCached / HBounded factories live on
`AStarLookup.Factory`.

## Inheritance
```
AlgoSPP[State]
    └── AStar[State]                   (simple, this class)
        ├── AStarLookup[State]            (advanced — i_2_astar_lookup/)
        └── Dijkstra[State]            (h=0 — i_2_dijkstra/)
```

## Tests
| File | Scope | Count |
|------|-------|-------|
| `_tester.py` | Graph problems + lifecycle + priority-shape pin | 8 |
| `_tester_grid.py` | Grid problems | 4 |
| `_tester_recording.py` | Full event-sequence (no Pro flags) | 6 |

18 tests total. Pro-side tests live in `i_2_astar_lookup/`.

## Why the split

Before this refactor, a single AStar class carried HCached +
HBounded + search_state + pathmax + to_cache machinery. That
meant every simple A* call paid:
1. `isinstance(h, HCached)` check at `__init__`.
2. 4-tuple priority with `is_perfect` call on every push/pop.
3. `is_cached` / `is_bounded` branches on every enriched event.
4. Propagate-event handling branch even when unused.

The split lets simple AStar skip all of that, keeping the hot
path tight for the common case while preserving full-featured
behaviour via the transparent `__new__` dispatch. Zero API
breakage for callers — `AStar(...)` still works the same way.

## Dependencies
- `f_hs.algo.i_0_base.AlgoSPP`
- `f_hs.frontier.i_1_priority.FrontierPriority`
- `f_hs.heuristic.i_0_base.HBase`
- `f_hs.heuristic.i_1_callable.HCallable`
- `f_hs.heuristic.i_1_cached.HCached` — for dispatch detection only
- `f_hs.heuristic.i_1_bounded.HBounded` — for dispatch detection only
