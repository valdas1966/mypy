# AlgoSPP

## Purpose
Abstract base class for SPP search algorithms. Implements the
classical search loop with eager deletion. Composes a
`FrontierBase` via constructor injection — subclasses inject
the appropriate frontier (FIFO for BFS, Priority for A*).
Recording is automatic inside `_push` and `_pop` (push / pop
events). The `decrease_g` op and its recording live on `AStar`
(`_decrease_g` is a priority-frontier-only operation), but the
generic `decrease_g` auto-fill (`g` + `parent`) stays in this
base's `_record_event`.

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
             is_recording: bool = False,
             search_state: SearchStateSPP[State] | None = None
             ) -> None
```

`search_state` — optional pre-built SearchStateSPP. When
supplied, the caller's bundle is wired to `self._search` (the
`frontier` argument is ignored). Use `resume()` (not `run()`)
to pump the seeded state; `run()` calls `_init_search()` which
clears the bundle. `_goals_set` is populated at init time —
the goal check works from the first `resume()` pop without
needing a prior `run()`.

Two use cases:
1. **Test seeding** — construct a state (some in `closed`,
   some on the frontier with specified `g` / `parent`) to pin
   behavior starting mid-search. See
   `algo/i_1_astar/_tester_recording.py ::
   test_recording_resume_from_seeded_search_state`.
2. **Iterative multi-query reuse** — hand an AStar's
   post-run bundle to a fresh AStar on a related problem for
   source-side savings. Paired with `to_cache()` (goal-side)
   this completes the two orthogonal reuse axes.

**Stale priorities — auto-refresh.** When `search_state` is
supplied, `AlgoSPP` sets an internal `_frontier_dirty=True`
flag. The next `resume()` call detects this, invokes
`refresh_priorities()` once, and clears the flag. The refresh
drains the frontier and re-pushes each state with a fresh
`_priority(state)` — AStar owns the priority computation, so
the caller doesn't have to duplicate it. Subsequent resume()
calls see a clean frontier and skip the refresh. `_init_search`
(called by `run()`) rebuilds the frontier from scratch and
also clears the flag.

### Methods
| Method | Signature | Description |
|--------|-----------|-------------|
| `run()` | `-> SolutionSPP` | Initialize and run, return solution |
| `resume()` | `-> SolutionSPP` | Continue without reinitializing; auto-refreshes stale frontier priorities on first call after a seed |
| `refresh_priorities()` | `-> None` | Drain the frontier and re-push every state with a fresh `_priority(state)`; callable anytime, no recorder events |
| `reconstruct_path()` | `(goal?) -> list[State]` | Trace parents |

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `search_state` | `SearchStateSPP[State]` | Dynamic per-search bundle |
| `counters` | `Counters` | 5-counter scaffold + 3 memory snapshots (`mem_open`, `mem_closed`, `mem_total`). Heap-op group (`cnt_push`, `cnt_pop`, `cnt_decrease`) is read from the injected frontier on every access — single source of truth. `cnt_push` / `cnt_pop` are always present on the frontier; `cnt_decrease` is **guarded** (`fc['cnt_decrease'] if 'cnt_decrease' in fc else 0`) — `FrontierPriority` reports the real count, while FIFO frontiers carry **no** `cnt_decrease` counter at all (decrease is not part of the FIFO interface), so a structural `0` is **synthesized at the algo level**. The algo-level scaffold still declares `cnt_decrease` for every algo, so the cross-algo comparison grid stays rectangular. Search-semantic group (`cnt_expanded`, `cnt_generated`) is incremented inline by the search loop and `_handle_child` (Stern-style "expanded" = popped state whose successors are generated; "generated" = first-time push, including the start seed). Memory group is reported in **node counts** (not `sys.getsizeof` bytes; switched 2026-06-25 for reproducibility), populated by `_run_post()` after the timer closes; `mem_open = frontier.max_size` (peak |OPEN|, rule-2 — see `f_hs/frontier/i_0_base/CLAUDE.md`), `mem_closed = len(closed)` at end (g / parent are not separate regions — a stored node is counted via its OPEN / CLOSED membership); `mem_total = Σ mem_*` is finalized last via `f_hs.algo.u_mem.finalize_mem_total` so subclass-added `mem_*` keys auto-absorb. Inherited unchanged by every concrete SPP algorithm (BFS, AStar, AStarLookup, AStarBPMX, Dijkstra); `AStarLookup` widens the scaffold to 13 names via per-class `_COUNTER_NAMES`, and `AStarBPMX` widens further to 16 via the same mechanism. |

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
    cache_hit:    State | None                    = None

    def clear(self) -> None: ...   # frontier.clear() + dicts/sets cleared
```

`cache_hit` is set by AStar's `_early_exit` when an `HCached`
heuristic is perfect at the popped state; `goal_reached` stays
None in that case. The two fields are mutually exclusive per
termination — at most one is set after a completed run.

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
        else: _relax_frontier_child(n, child, new_g)
```

The final `else` branch routes through the
`_relax_frontier_child` hook. The base default is a **no-op**
(insertion-order FIFO / BFS frontiers never relax). `AStar`
overrides it: `if new_g < g(child): adopt (g + parent); decrease`
— `decrease` is a priority-frontier-only op and lives on `AStar`.

## Event Recording
Recording is automatic inside `_push` and `_pop` (push / pop);
`AStar._decrease_g` records the `decrease_g` event. The
`decrease_g` field auto-fill (`g` + `parent`) lives in this
base's `_record_event`. Three event types, duration in
nanoseconds:

| Event | Fields |
|-------|--------|
| `push` | state, g, parent, duration |
| `pop` | state, g, duration |
| `decrease_g` | state, g, parent, duration |

`g` is recorded as **`int`** (cast for safety). The internal
`self._search.g` is now **int** too: the start is seeded as
`0` (not `0.0`, fixed 2026-06-12) and `problem.w` returns int
`1` by default, so g stays int for the integer-cost problems
(unit-cost BFS/A*/Dijkstra) — matching `KAStarAgg`'s int g.
Fractional-weighted edges promote g to float naturally
(`int + float = float`), identically across all SPP algos.

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
| `g` (answer) | ✓ | ✓ | ✓ | answer at each event; cast to `int` |
| `parent` | ✓ | ✓ | ✗ | structural — constant since last push/decrease_g |
| `w` | ✗ | ✗ | ✗ | derivable as `g(child) − g(parent)` |
| `h`, `f` (AStar) | ✓ | ✓ | ✓ | enriched on all three; cast to `int` when integer-valued |
| `duration` | ✓ | ✓ | ✓ | generic, via `ProcessBase` |

Why `g` stays on every event (not "constant since push"):
it's the *answer* the algorithm delivers. The canonical
expansion-order query
`[(e['state'], e['g']) for e in events if e['type']=='pop']`
works without replaying the push/decrease_g log — a strong
consumer-convenience argument that overrides strict minimalism
for this one field.

`g` is recorded as **`int`** (cast for safety). Internal
`self._search.g` is **int** (start seeded `0`, `w` returns int
`1`; fixed 2026-06-12 for cross-algo consistency with
`KAStarAgg`). `float('inf')` is **never stored in `g`** — it
appears only in `SolutionSPP.cost` for unreachable states
(`main.py` returns `SolutionSPP(cost=float('inf'))`), so the
int-g change does not affect unreachable handling. Fractional
weights promote g to float naturally.

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
| `_relax_frontier_child(parent, child, new_g)` | no-op | Re-encountered a child already on the frontier. Base default: no-op (insertion-order FIFO / BFS never relax). `AStar` overrides — `if new_g < g(child)`: adopt `g` + `parent` and `_decrease_g(child)` (priority-frontier-only). |
| `_enrich_event(event)` | no-op | Add fields to recorded events |
| `_is_goal(state)` | `state in _goals_set` | Goal check |
| `_init_search()` | clears `_search`, rebuilds `_goals_set`, pushes starts | Override for OMSPP-style multi-pump init |
| `_search_loop()` | classical SPP loop | Override for OMSPP / bidirectional / etc. |
| `_early_exit(state)` | returns `None` | Return `SolutionSPP` to short-circuit the loop after pop; AStar uses this for `HCached` perfect-h termination |
| `_PRESEARCH_COUNTER_NAMES` (class attr) | `()` | Names of counters that describe work done OUTSIDE the search loop. Preserved across `_init_search`'s `_counters.reset()` so post-`run()` snapshots reflect both pre-search and search work — same retention principle as the recorder (which is also not cleared by `_init_search`). `AStarLookup` overrides with the propagate group (`cnt_prop_waves` / `cnt_prop_attempts` / `cnt_prop_lifts`); `AStarBPMX` inherits unchanged because its `cnt_bpmx_*` group is in-search and is correctly subject to reset. |

Event types recorded by this base class: `push`, `pop` (the
`decrease_g` event is emitted by `AStar._decrease_g`, though
its `g` / `parent` auto-fill lives in this base's
`_record_event`). Subclasses may emit additional types:

- **AStarLookup** adds two pre-search pathmax event types:
  - `propagate_wave` — state-less meta-event at the start of
    each wave that runs. Schema: `{type, depth, num_sources}`.
  - `propagate` — one per (source, child) attempt during pre-
    search. Schema: `{type, state, parent, h_parent, h,
    was_improved}`.
  `was_improved=True` on strict tightening, `False` on no-op
  attempt — present on every propagate event. This is an
  **event-outcome** flag (did this attempt tighten?), distinct
  from the **state-property** `is_bounded` on push/pop (does
  this state have a tight bound?). A state that is
  `is_bounded=True` at search time can still generate
  `was_improved=False` propagate events during pathmax when
  later attempts fail to tighten it further. Propagate events
  never carry `is_bounded` or `is_cached`. No `g` / `f`
  (pre-search; not applicable). `h` / `h_parent` cast to int
  when integer-valued (shared with AStar's `_enrich_event`
  cast logic for `push` / `pop` / `decrease_g`).
- **AStarBPMX** (when `rule_bpmx is not None`) adds four
  in-search Felner-pathmax event types: `pathmax_apply`
  (isolated Rule 2), `bpmx_iteration` (cascade round-marker),
  `bpmx_lift` (Rule 3 fired), `bpmx_forward` (Rule 1 fired).
  See `f_hs/algo/i_0_oospp/mixins/bpmx/CLAUDE.md`.

AStar also adds flags on `push` / `pop`:
- `is_cached=True` for states with `is_perfect` True (HCached
  hit). The terminator is readable as "the last pop carrying
  `is_cached=True`".
- `is_bounded=True` on push/pop of states whose h is strictly
  tightened by an HBounded bound.

All flags are **absent** (not False) on non-applicable events —
constant-False flags violate the Recording Principle.

**`_record_event(type, state, **extra)`** — auto-fills `g`
for `push` / `pop` / `decrease_g`, and `parent` for
`push` / `decrease_g`. Other event types receive no auto-fill;
callers pass context via `**extra` (e.g., pathmax passes
`parent=source, h_parent=..., h=...` for propagate events).

**Recorder is NOT cleared** by `_init_search()` — pre-search
events from `propagate_pathmax` persist into the search log.
Callers wanting a fresh log across repeated `run()` calls
clear explicitly via `self.recorder.clear()`.

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
