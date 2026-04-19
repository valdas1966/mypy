# AlgoSPP

## Purpose
Abstract base class for SPP search algorithms. Implements the
classical search loop with eager deletion. Composes a
`FrontierBase` via constructor injection — subclasses inject
the appropriate frontier (FIFO for BFS, Priority for A*).
Recording is automatic inside `_push`, `_pop`, and `_decrease_g`.

The dynamic per-search state (frontier + g + parent + closed +
goal_reached) lives in a single `SearchStateSPP` dataclass on
`self._search`, enabling `resume()` (continue without
re-initializing) and read-only inspection across instances (for
bidirectional search).

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
             frontier: FrontierBase[State],
             name: str = 'AlgoSPP',
             is_recording: bool = False) -> None
```

### Methods
| Method | Signature | Description |
|--------|-----------|-------------|
| `run()` | `-> SolutionSPP` | Initialize and run, return solution |
| `resume()` | `-> SolutionSPP` | Continue without reinitializing |
| `reconstruct_path()` | `(goal?) -> list[State]` | Trace parents |

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `search_state` | `SearchStateSPP[State]` | Dynamic per-search bundle |

### Inherited from Algo / ProcessBase
| Property / Method | Description |
|----|----|
| `problem` | The input problem |
| `elapsed` | Execution time (seconds) — reset on every `run()` and `resume()` |
| `recorder` | Event recorder (cleared by `_init_search`, NOT by `resume`) |
| `_record_event` | Inherited from ProcessBase |
| `_enrich_event` | Override hook (AStar adds h/f) |

## SearchStateSPP — the per-search bundle

Defined in `_search_state.py`, exported through `__init__.py`.
Five mutable fields, all reset by `clear()`:

```python
@dataclass
class SearchStateSPP(Generic[State]):
    frontier:     FrontierBase[State]
    g:            dict[State, float]              = field(default_factory=dict)
    parent:       dict[State, State | None]       = field(default_factory=dict)
    closed:       set[State]                      = field(default_factory=set)
    goal_reached: State | None                    = None

    def clear(self) -> None: ...   # frontier.clear() + dicts/sets cleared
```

Why a dataclass instead of five flat attributes:

1. **Resumability** — `resume()` re-enters `_search_loop` without
   touching this bundle, so frontier/closed/g/parent persist.
2. **Cross-instance inspection** — bidirectional search needs to
   peek at the *other* side's `closed` and `g` to detect meeting
   and compute candidate paths; the `search_state` property
   exposes the bundle as a single object.
3. **Subclass extension** — OMSPP adds `goals_reached: set[State]`
   and `solutions: dict[State, SolutionSPP]` on a
   `SearchStateOMSPP(SearchStateSPP)`, without touching the SPP
   shape.

What is **NOT** in `SearchStateSPP`:
- **`goals_set`** — derived from the immutable problem.goals;
  cached directly on `AlgoSPP._goals_set`. It does not change
  across `run` / `resume` cycles, so it does not belong in the
  *dynamic* state bundle.
- **h-values cache** — currently unused (h is a callable on
  AStar, recomputed per call). If a future profile justifies
  caching, add `dict_h: dict[State, float]` here as a separate,
  motivated change.

## Lifecycle — `run()` vs `resume()`

```
run()        →  _run_pre  →  _run             →  _run_post
                            ├── _init_search  (clears _search,
                            │                  rebuilds _goals_set,
                            │                  clears recorder,
                            │                  pushes starts)
                            └── _search_loop  (the while-frontier loop)

resume()     →  _run_pre  →  _search_loop     →  _run_post
                            (NO _init_search; NO recorder.clear)
```

- `run()` is the inherited entry point; calls `_run()` which
  initializes from scratch and pumps the loop.
- `resume()` is a **new** entry point that piggybacks on the same
  `_run_pre`/`_run_post` plumbing (timing reset + output capture)
  but skips initialization. The recorder accumulates across
  `run()` + `resume()` calls — exactly what OMSPP-iterative
  recording needs.
- After `resume()`, `algo.elapsed` reports time of just the
  resumed pump, not cumulative.

## Search Loop (Classical Pseudocode)
```
FRONTIER ← {start}             # _init_search (run() only)
while FRONTIER:                # _search_loop (run() and resume())
    n ← FRONTIER.pop_min()
    if n is goal: return cost
    CLOSED ← CLOSED ∪ {n}
    for each child of n:
        if child in CLOSED: skip
        w ← problem.w(n, child)
        if child not in FRONTIER: insert
        else if new_g < g(child): decrease
```

## Event Recording
Recording is automatic inside `_push`, `_pop`, `_decrease_g`.
Three event types, duration in nanoseconds:

| Event | Fields |
|-------|--------|
| `push` | state, g, parent, duration |
| `pop` | state, g, duration |
| `decrease_g` | state, g, parent, duration |

`g` is recorded as **`int`** (cast from internal float).
Assumption: edge costs are integer-valued — holds for all
current problems (unit-cost BFS/A*/Dijkstra). Revisit when
introducing fractional-weighted edges.

`parent` carries the `State` object (or `None` for starts).
AStar enriches all three event types with `h` and `f = g + h`.

### Recording Principle (framework-wide)

Each event records:
1. **What is newly determined at this event** (the value(s)
   decided or changed right now).
2. **What makes the event self-describing for its primary
   consumer** (the "answer" the event exists to deliver).

Events **never** record:
- values that are constant since the last related event
  (structural / unchanged info), or
- values that are derivable from the event log.

This gives **variable schemas per event type** — a pop event
has no `parent` key, not a `parent=None` key. The distinction
matters:

- `'parent' in event` → "this kind of event describes
  parenthood; here's its value (or `None` for a start)."
- `'parent' not in event` → "parenthood is not applicable
  to this kind of event."

Collapsing both into a uniform-schema with `parent=None`
would conflate "no parent (start state)" with "not applicable
(pop)" — and silently admits schema drift (e.g., accidentally
setting `parent` on a pop).

### Concrete field map for SPP search

| Concern | push | decrease_g | pop | Reason |
|---------|:----:|:----------:|:---:|--------|
| `state` | ✓ | ✓ | ✓ | subject |
| `g` (answer) | ✓ | ✓ | ✓ | answer at each event |
| `parent` | ✓ | ✓ | ✗ | structural — constant since last push/decrease_g |
| `w` | ✗ | ✗ | ✗ | derivable as `g(child) − g(parent)` |
| `h`, `f` (AStar) | ✓ | ✓ | ✓ | enriched on all three |
| `duration` | ✓ | ✓ | ✓ | generic, via `ProcessBase` |

Why `g` stays on every event (not "constant since push"):
it's the *answer* the algorithm delivers. The canonical
expansion-order query
`[(e['state'], e['g']) for e in events if e['type']=='pop']`
works without replaying the push/decrease_g log — a strong
consumer-convenience argument that overrides strict minimalism
for this one field.

`g` is recorded as **`int`** (cast from internal float).
Assumption: edge costs are integer-valued — holds for all
current problems. Revisit when introducing fractional weights.
Internal `self._search.g` stays float so `float('inf')` remains
usable for unreachable states.

### Future-proofing

If event types multiply (OMSPP `goal_reached`, incremental A*
`reopen`, bidirectional `frontier_id`, LPA* `recompute`), each
new type adds its *own* fields without touching existing ones.
When the number of event types or fields grows uncomfortable,
`TypedDict` per event type is the natural next step — pinning
schemas at the type level with zero runtime cost.

## Internal Data
| Attribute | Type | Description |
|-----------|------|-------------|
| `_search` | `SearchStateSPP[State]` | Dynamic per-search bundle (5 fields) |
| `_goals_set` | `set[State]` | Cached goal lookup (problem-derived, static) |

The five fields previously held as separate `self._frontier`,
`self._g`, `self._parent`, `self._closed`, `self._goal_reached`
attributes now live inside `self._search`. Read them as
`self._search.frontier`, `self._search.g[...]`, etc. Subclass
overrides (e.g. AStar's `_priority`) reference them through
`self._search`.

## Hooks for Subclasses
| Hook | Default | Purpose |
|------|---------|---------|
| `_priority(state)` | `None` | Priority for frontier push/decrease |
| `_enrich_event(event)` | no-op | Add fields to recorded events |
| `_is_goal(state)` | `state in _goals_set` | Goal check |
| `_init_search()` | clears `_search`, rebuilds `_goals_set`, pushes starts | Override for OMSPP-style multi-pump init |
| `_search_loop()` | classical SPP loop | Override for OMSPP / bidirectional / etc. |

Previously (pre-2026-04-16) AlgoSPP also required `_frontier_push`,
`_frontier_pop`, `_has_frontier`, `_in_frontier`,
`_frontier_decrease`. These are gone — `self._search.frontier`
handles them directly via its narrow interface.

## Dependencies
- `f_cs.algo.Algo`
- `f_hs.problem.ProblemSPP`
- `f_hs.solution.SolutionSPP`
- `f_hs.state.StateBase`
- `f_hs.frontier.FrontierBase`
