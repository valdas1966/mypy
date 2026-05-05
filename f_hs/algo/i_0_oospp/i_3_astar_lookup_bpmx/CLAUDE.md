# AStarLookupBPMX

## Purpose

A* enhanced by **lookup tables** (cache, bounds, pre-search
pathmax) **and** in-search **Felner pathmax / BPMX(d)** in
one pass. Composes `AStarLookup` (cache + bounds + pre-search)
with `BPMXMixin` (in-search Felner mechanism) — the Phase-2
integration class used by `KAStarCB` for OMSPP / MOSPP
sub-search where every reuse axis must compose.

Sibling: `AStarBPMX` (BPMX without cache) and `AStarLookup`
(cache without BPMX). All three sit at `i_2_*` / `i_3_*`
under `f_hs/algo/`. The shared in-search mechanism lives in
`f_hs/algo/i_0_oospp/mixins/bpmx/main.py`.

## Public API

### Constructor
```python
AStarLookupBPMX(
    problem: ProblemSPP[State],
    h: HBase[State] | Callable[[State], int] | None = None,
    name: str = 'AStarLookupBPMX',
    is_recording: bool = False,
    search_state: SearchStateSPP[State] | None = None,
    cache: dict[State, CacheEntry[State]] | None = None,
    goal: State | None = None,
    bounds: dict[State, float] | None = None,
    rule_bpmx: str | None = None,
    depth_bpmx: int | None = 1,
)
```

Kwargs split:
- **AStarLookup-side**: `cache`, `goal`, `bounds`. Same
  semantics as `AStarLookup` — see its CLAUDE.md.
- **BPMX-side**: `rule_bpmx ∈ {None, '1', '2', '3', 'CASCADE'}`,
  `depth_bpmx ∈ {None, int >= 1}`. Same semantics as
  `AStarBPMX` / `BPMXMixin` — see `oospp/mixins/bpmx/` and
  `BPMXMixin` docstring.

### Storage auto-wrap

When `rule_bpmx is not None` AND `h` is a callable / None AND
`bounds` is None, the constructor synthesizes an empty
`bounds={}` so AStarLookup's chain builder includes the
HBounded layer needed as storage for lifted h-values. With a
pre-built HBase chain, the host must supply HBounded
(constructor verifies; ValueError otherwise).

### Validation (rejected configurations)

| Input | Error | Source |
|---|---|---|
| `rule_bpmx not in {None, '1', '2', '3', 'CASCADE'}` | `ValueError` | BPMXMixin |
| `depth_bpmx not in {None} ∪ {int >= 1}` | `ValueError` | BPMXMixin |
| `rule_bpmx == '2'` with `depth_bpmx != 1` | `ValueError` | BPMXMixin (Rule 2 cannot propagate) |
| `cache` without `goal` | `ValueError` | AStarLookup |
| Pre-built `HBase` `h` + `cache` / `bounds` | `ValueError` | AStarLookup |
| HCached goal not in `problem.goals` | `ValueError` | AStarLookup |
| Mechanism on but no HBounded in chain | `ValueError` | this class |

## Combined-Class MRO

```
AStarLookupBPMX → BPMXMixin → AStarLookup → AStar
                → AlgoSPP → ... → object
```

Method resolution:

| Method | Resolves to | Why |
|---|---|---|
| `_pre_expand` | `BPMXMixin` | mechanism orchestrator |
| `_early_exit` | `AStarLookup` | HCached perfect-h |
| `_priority` | `AStarLookup` | 4-tuple cache_rank |
| `reconstruct_path` | `AStarLookup` | suffix-stitch |
| `to_cache` | `AStarLookup` | harvest |
| `propagate_pathmax` | `AStarLookup` | pre-search waves |
| `counters` | `BPMXMixin` | 15-name scaffold (3 prop + 3 bpmx + 3 frontier + 2 search-semantic + 4 memory) |
| `_enrich_event` | `BPMXMixin → AStarLookup → AStar` | chained via `super()` |

The `_enrich_event` chain runs in MRO order: BPMXMixin first
calls `super()._enrich_event(event)` which routes to
AStarLookup → AStar (h, f, is_cached, is_bounded, propagate
casts), then BPMXMixin adds its `pathmax_apply` / `bpmx_lift`
/ `bpmx_forward` int-casts.

## Counters

15-name scaffold declared via `_COUNTER_NAMES` (per-class
override of `BPMXMixin._BPMX_COUNTER_NAMES` to add the
`cnt_prop_*` group inherited from AStarLookup):

```
propagate (3) — pre-search waves on AStarLookup:
  cnt_prop_waves         -- waves run by propagate_pathmax
  cnt_prop_attempts      -- (source, child) attempts
  cnt_prop_lifts         -- successful tightenings

bpmx (3) — in-search mechanism (any rule_bpmx):
  cnt_bpmx_attempts      -- _pre_expand calls when rule_bpmx is set
  cnt_bpmx_successes     -- successful lifts (cumulative)
  cnt_bpmx_depth         -- max BFS-level at which a lift fired

frontier (3, mirrored from FrontierPriority on every read):
  cnt_push, cnt_pop, cnt_decrease

search-semantic (2, inherited from AlgoSPP):
  cnt_expanded, cnt_generated

memory (4, post-run snapshot):
  mem_open, mem_closed, mem_cache, mem_bounds
```

`cnt_bpmx_cascade_successes` is the sum of Rule 3 lifts +
Rule 1 forwards across all cascades. `cnt_bpmx_cascade_total_depth`
gives cumulative BFS depth — average cascade depth is
Per-rule lift breakdown and iteration count remain visible
via `bpmx_lift` / `bpmx_forward` / `pathmax_apply` /
`bpmx_iteration` recording events for diagnostic runs.

**Cache-hit interaction**: when a cached state is popped,
`_early_exit` fires BEFORE `_pre_expand`, so the cascade does
NOT run for that pop. `cnt_bpmx_attempts` therefore can be
strictly less than the count of non-goal pops when the cache
covers any expansion target.

## Recording event types

In addition to AStar's `push` / `pop` / `decrease_g`:

From AStarLookup:
- `propagate_wave`, `propagate` (pre-search; from
  `propagate_pathmax`).
- Event flags `is_cached` / `is_bounded` on push / pop.

From BPMXMixin:
- `pathmax_apply{rule=2}` — Rule 2 lifts (depth-1 only).
- `bpmx_lift` — Rule 3 lifts (alone or in cascade).
- `bpmx_forward` — Rule 1 pushes (alone or in cascade).
- `bpmx_iteration` — CASCADE round-marker (cascade only).

A cached state in the cascade subtree is skipped from lift
mutation (`_h.is_perfect(c)` guard in the mixin) — no
`bpmx_lift` / `bpmx_forward` event names a cached state.

## Inheritance

```
AlgoSPP[State]
  └── AStar[State]
        ├── AStarLookup[State]    (cache + bounds + propagate_pathmax)
        │     └── AStarLookupBPMX (this class — composes BPMXMixin)
        └── AStarBPMX[State]      (BPMX-only sibling)
```

## Factory

| Method | Cache | Notes |
|---|:---:|---|
| `graph_abc_cached_at_b(rule_bpmx=None, depth_bpmx=1, is_recording=False)` | yes | Parametric on graph_abc with cache covering {B, C}. Defaults = off-mode (matches `AStarLookup.Factory.graph_abc_cached_at_b()`); active mechanisms (e.g. `rule_bpmx='CASCADE', depth_bpmx=1, is_recording=True`) exercise the combined cache + BPMX path. |
| `grid_4x4_no_cache(rule_bpmx=None, depth_bpmx=1)` | no | Parametric on the canonical 4x4 grid with Manhattan h. Mirrors `AStarBPMX.Factory.grid_4x4(...)` for the no-cache equivalence side. Defaults = off-mode; e.g. `grid_4x4_no_cache(rule_bpmx='CASCADE', depth_bpmx=None)` matches AStarBPMX BPMX(∞), `grid_4x4_no_cache(rule_bpmx='3')` matches Rule 3. |
| `grid_4x4_cached_suffix_cascade_d1()` | yes | cached-goal only + CASCADE depth=1 |
| `graph_diamond_inconsistent_cascade()` | no | inconsistent toy + CASCADE(∞), `is_recording=True` |

## Tests

| File | Scope | Count |
|---|---|---:|
| `_tester.py` | validation, optimality (16 no-cache combos × 3 with-cache), off-matches-AStarLookup, BPMX-matches-AStarBPMX, cache-hit early term + BPMX, to_cache, propagate_pathmax, suffix-stitch, subclass, factory, MRO | 35 |
| `_tester_recording.py` | Full event-stream pin (single `actual == expected` assertion against the normalized event list, `duration` stripped) on the canonical OOSPP problem with full BPMX cascade — covers `bpmx_iteration` markers in the AStar trace. Cache- and bounds-driven scenarios live in `_tester_recording_others.py`. | 1 |
| `_tester_counters.py` | scaffold shape, off-mode pin, mechanism counters per expansion, cache-hit skips BPMX, two pinned-value cases, recording-independence | 10 |

54 tests total; all green.

## Dependencies
- `f_hs.algo.i_0_oospp.mixins.bpmx.BPMXMixin` (in-search mechanism)
- `f_hs.algo.i_2_astar_lookup.AStarLookup` (cache + bounds)
- `f_hs.heuristic.i_0_base.HBase` + `CacheEntry`
- `f_hs.heuristic.i_1_*` chain layers (HCached / HBounded /
  HCallable; via AStarLookup's chain builder)
