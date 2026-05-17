# AStarIncMOSPP — Incremental k×A* (MOSPP)

## Purpose

Solves the Many-to-One Shortest Path Problem (MOSPP): the
shortest path from each of `k` starts `[s₁, …, sₖ]` to a
shared single goal `t`.

Runs `k` sequential **forward** `AStarBPMX` sub-searches, one
per start. Unlike `AStarRepMOSPP` (the no-sharing baseline),
each sub-search **carries forward** what earlier ones learned.
Because the start varies, the `SearchStateSPP` bundle does NOT
transfer (OPEN/CLOSED/g/parent are start-relative); instead
two **goal-anchored** stores accumulate (the goal is fixed, so
they stay valid across sub-searches):

- **on-path cache** `cache[x] = h*(x, t)` — harvested by
  `AStarLookup.to_cache()` after each reached sub-search.
- **admissible bounds** `bounds[x] ≥ h*(x, t)` — SPI
  (`C_i − g_i(x)` for CLOSED x) + the inner `HBounded` layer
  (BPMX-lifted / pathmax-propagated values).

**Headline win — cache-hit-at-init.** If a later start `s_j`
is already in the carried cache, the inner `AStarLookup` pops
it on the first iteration and `_early_exit` terminates the
sub-search in ONE pop, zero expansions, cost `h*(s_j, t)`.

Mirror of `AStarRepMOSPP._handle_start` with two diffs:
cache-hit-at-init accounting + `to_cache` / `_harvest_bounds`
reuse plumbing. The inner algo is `AStarBPMX` (subsumes
`AStarLookup`; `rule_bpmx=None` ⇒ identical to `AStarLookup`),
so cache, bounds, pre-search `propagate_pathmax`, and in-search
BPMX are all reachable through one inner class.

## Public API

### Constructor

```python
AStarIncMOSPP(problem: ProblemSPP[State],
              h: Callable[[State, State], int],
              name: str = 'AStarIncMOSPP',
              is_recording: bool = False,
              is_timing: bool = True,
              order_starts: str = 'near',
              carry_cache: bool = True,
              carry_bounds: bool = True,
              propagate: bool = False,
              propagate_depth: int | None = None,
              rule_bpmx: str | None = None,
              depth_bpmx: int | None = 1)
```

- `problem.starts` = `[s₁, …, sₖ]`; `problem.goals` must have
  **exactly one** goal (else `ValueError`).
- `h(state, goal) -> int` — bi-arg, admissible. Goal is fixed
  ⇒ the counter-wrapped unary h is built once and reused (also
  the `order_starts` metric — raw, not counted).
- `order_starts ∈ {near, far, mean, random}`:
  - `near`/`far` — ascending / descending by `h(start, goal)`.
  - `mean` — ascending by `|h(start, goal) − mean|`.
  - `random` — deterministic shuffle (fixed seed `0`).
- `carry_cache` / `carry_bounds` — replay the respective
  goal-anchored store across sub-searches.
- **`propagate` is a separate boolean from `propagate_depth`.**
  `propagate_pathmax(depth=None)` means "run to convergence",
  which is distinct from "do not propagate". Without the
  boolean the cache-only config and the propagate-to-
  convergence config would be byte-identical kwargs.
- `rule_bpmx` / `depth_bpmx` — forwarded to the inner
  `AStarBPMX` (`None` ⇒ BPMX off).

### Methods

| Method | Description |
|---|---|
| `run() -> SolutionMOSPP` | Orchestrate k sequential sub-searches over the policy-ordered starts. |
| `reconstruct_path(start) -> list[State]` | Returns `[]` by design — sub-search parent pointers are discarded (mirror of `AStarRepMOSPP`). |

### Counter scaffold

| group | counters |
|---|---|
| h | `cnt_h_search` (orchestrator-owned; wrapped h) |
| propagate | `cnt_prop_waves` (MAX-aggregated — see below), `cnt_prop_attempts`, `cnt_prop_lifts` |
| bpmx | `cnt_bpmx_attempts`, `cnt_bpmx_successes`, `cnt_bpmx_depth` |
| frontier | `cnt_push`, `cnt_pop`, `cnt_decrease` |
| search | `cnt_expanded`, `cnt_generated` |
| reuse | `cnt_cache_hits_at_init` |
| memory | `mem_open`, `mem_closed` (peak across sub-searches) |

Inner-`AStarBPMX` counters are **summed** across
sub-searches, with two exceptions:
- **`cnt_prop_waves` is MAX-aggregated, not summed.** It is
  a propagation-DEPTH horizon — *the deepest wave ladder any
  single sub-search ran* — not total wave-work. Rationale:
  per sub-search, `propagate_pathmax(depth)` runs ≤ `depth`
  waves; summing across k sub-searches conflates depth with
  count and surprises (`depth_1` would read k−1, not 1). The
  wave *work* is already carried by the summed
  `cnt_prop_attempts` / `cnt_prop_lifts`, so MAX loses no
  information. Mirrors the peak aggregation of `mem_open` /
  `mem_closed` (see `_prop_waves_peak`, flushed in
  `_sync_memory_snapshot`). The first sub-search typically
  contributes 0 (empty carried cache ⇒ no propagate seeds);
  on the canonical fixture `depth_1/2/3 → 1/2/3`,
  `depth_inf → 5`. OMSPP `KAStarInc` never propagates so
  `cnt_prop_waves ≡ 0` there — SUM and MAX coincide; this
  redefinition is MOSPP-only by nature.
- `cnt_h_search` is incremented directly by the wrapped h
  (no inner counter).

`cnt_cache_hits_at_init` is orchestrator-owned. No
`cnt_h_update` (no PHASE_UPDATE); `elapsed_update` ≡ 0.0.

## Recording — event schema

| event | source |
|---|---|
| `push` / `pop` / `decrease_g` | inner `AStarBPMX` (with `is_cached` / `is_bounded` flags from the lookup layers) |
| `propagate_wave` / `propagate` | pre-search `propagate_pathmax` (when `propagate=True`) |
| `pathmax_apply` / `bpmx_iteration` / `bpmx_lift` / `bpmx_forward` | in-search BPMX (when `rule_bpmx` set) |
| `cache_hit_at_init` | sub-search terminated on first pop via the carried cache. Payload: `state, g, start_index` |
| `on_start` | per start at sub-search end. `reason ∈ {expanded, already_reached, unreachable}`; payload `state, g, reason, start_index` |
| `update_frontier` | **NEVER emitted** (no shared frontier) |

`already_closed` is never emitted (no shared CLOSED set).

## Algorithm

```
order starts by `order_starts`
cache, bounds = {}, {}
for i, s_i in enumerate(ordered_starts):
    if s_i in solutions:                      # duplicate start
        emit on_start(already_reached); continue
    algo = AStarBPMX(single_start_view(s_i), h=h_wrapped,
                      cache=cache?, goal=t, bounds=bounds?,
                      rule_bpmx=…, depth_bpmx=…)
    algo._recorder = self._recorder
    if propagate: algo.propagate_pathmax(propagate_depth)
    sol = algo.run()                          # may cache-hit-at-init
    accumulate inner counters
    if cache-hit on first pop: cnt_cache_hits_at_init++ ;
                               emit cache_hit_at_init
    emit on_start(expanded | unreachable)
    if reached:
        if carry_cache: cache.update(algo.to_cache())
        if carry_bounds: harvest SPI + HBounded into bounds
```

## Factory

| Method | Description |
|---|---|
| `canonical(**kwargs)` | `grid_6x6_zigzag_mospp` (starts (0,0)/(2,3)/(0,3); goal (5,0); costs 15/10/12). `**kwargs` override the config. |
| `graph_abc_two_starts()` | A→B→C, starts [A,B], goal C. Sub-search 2 (B) reuses sub-search-1 cache mid-search. |
| `graph_abc_repeated_start()` | starts [A,A], goal B. Sub-search 2 → `already_reached` fast-path. |

## Tests

| File | Scope | Count |
|---|---|---|
| `_tester.py` | lifecycle: canonical + cache-hit-at-init, multi-goal / bad-policy rejection, duplicate-start fast-path, all 4 order policies correct, `elapsed_update==0`, no `update_frontier`, empty `reconstruct_path`, carry-cache toggle | 9 |
| `_tester_counters.py` | one method per param config (18: 1 cache + 4 propagate + 13 BPMX); full non-mem counter dict + per-start costs pinned from the Phase-0b oracle | 18 |
| `_tester_recording.py` | one method per param config (18); full normalized event-stream golden master | 18 |

**Group C uses `carry_cache=True`.** The sub-search-1 on-path
cache is BPMX's inconsistency engine on the otherwise-
consistent Manhattan h (same role as the cached beacon in
`AStarBPMX`'s OOSPP testers — see
`i_3_astar_bpmx/CLAUDE.md`). With `carry_cache=False` Rules 1
and 3 never lift and `rule_1_depth_1 == rule_3_depth_1`
(verified collision); with the cache present all 18 tuples are
distinct.

`study/oracle.py` (script-only — no CLAUDE.md) dumps the 18
counter tuples and asserts distinctness; it is the source of
the `_tester_counters.py` pins. Run:
`python -m f_hs.algo.i_1_mospp.i_1_astar_inc.study.oracle`.

`COUNTERS.html` is the human-eye view of the same data: an
18-config × 8-counter param-sensitivity heatmap (each
column heat-scaled independently min→max; only
param-discriminating counters are shown — every shown
column moves), grouped A/B/C with the fixture and the
design-decision callouts.
**Five counters are omitted from the heatmap** (all kept
in the class scaffold / `_tester_counters.py`):
- `cnt_decrease` — invariant `≡ 0` (no priority-decrease
  on this all-reachable unit-cost fixture).
- `cnt_cache_hits_at_init` — the algorithm's **headline**
  metric, NOT vestigial. Constant `= 1` here only because
  every config carries the cache and the S1→T optimal-path
  geometry is param-independent (exactly S2 lands on it):
  the invariance is **fixture-geometry**, not structural.
  Across fixtures it ranges `[0, k−1]` and is the sole
  counter-side (recording-OFF) witness of the
  cache-hit-at-init win — not derivable from the aggregate
  frontier/search counters (the `cnt_pop ≡ cnt_expanded+k`
  identity is blind to it). Surfaced via the fixture
  callout + `study/oracle.py` / `_tester_counters.py`, just
  not as a flat heatmap column.
- `cnt_push` / `cnt_pop` — affine duplicates on this
  all-reachable unit-cost fixture: given `cnt_decrease ≡ 0`,
  `cnt_push ≡ cnt_generated` and `cnt_pop ≡
  cnt_expanded + k` (k=3 starts). The generator asserts
  the identity (a fixture that breaks it re-surfaces them).
- `cnt_h_search` — dropped by request (pure
  heuristic-evaluation cost). It is the **sole** separator
  of two BPMX depth tails, so on the shown counters only
  **12 of 18** configs differ; the 6 collapsed configs are
  tagged `≡ <canonical>` and dimmed, and the badge reads
  `12 / 18` (amber). Full 18-way distinctness (incl.
  `cnt_h_search` / push / pop) is the contract verified by
  `study/oracle.py` and `_tester_counters.py` — COUNTERS.html
  is a readability view, not the distinctness oracle.

Regenerate after any counter-affecting change so it tracks
`_tester_counters.py`. Dark-themed, self-contained; for
human reading only (Claude reads CLAUDE.md).

## Assumptions & limitations

1. **Admissible h** (cache holds exact h*; SPI / HBounded are
   admissible LBs). Consistency NOT required — BPMX exists for
   inconsistent h.
2. **Exactly one goal** — `ValueError` at construction
   otherwise.
3. **Non-negative edge costs** (inherited from `ProblemSPP` /
   A* correctness).
4. **Path reconstruction unsupported** — sub-search bundles
   discarded.

## Dependencies

- `f_hs.algo.i_1_mospp.i_0_base.AlgoMOSPP` (base: lifecycle +
  counter scaffold).
- `f_hs.algo.i_1_mospp._single_start_view._SingleStartView`.
- `f_hs.algo.i_0_oospp.i_3_astar_bpmx.AStarBPMX` (inner
  sub-search; subsumes `AStarLookup`).
- `f_hs.heuristic.i_1_bounded.HBounded`,
  `f_hs.heuristic.i_0_base.CacheEntry`.
- `f_hs.problem.i_0_base.ProblemSPP`.
- `f_hs.solution.SolutionMOSPP`, `f_hs.solution.SolutionSPP`.
