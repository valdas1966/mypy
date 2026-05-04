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
    rule_pathmax: int | None = None,
    depth_bpmx: int | None = 0,
)
```

Kwargs split:
- **AStarLookup-side**: `cache`, `goal`, `bounds`. Same
  semantics as `AStarLookup` — see its CLAUDE.md.
- **BPMX-side**: `rule_pathmax ∈ {None, 1, 2, 3}`, `depth_bpmx ∈
  {0, n ≥ 1, None}`. Same semantics as `AStarBPMX` /
  `BPMXMixin` — see `oospp/mixins/bpmx/` and `BPMXMixin` docstring.

### Storage auto-wrap

When a BPMX mechanism is enabled (`rule_pathmax` set OR
`depth_bpmx > 0` OR `depth_bpmx is None`) AND `h` is a
callable / None AND `bounds` is None, the constructor
synthesizes an empty `bounds={}` so AStarLookup's chain
builder includes the HBounded layer needed as storage for
lifted h-values. With a pre-built HBase chain, the host
must supply HBounded (constructor verifies; ValueError
otherwise).

### Validation (rejected configurations)

| Input | Error | Source |
|---|---|---|
| `rule_pathmax not in {None, 1, 2, 3}` | `ValueError` | BPMXMixin |
| `depth_bpmx not in {None} ∪ {int >= 0}` | `ValueError` | BPMXMixin |
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
| `counters` | `BPMXMixin` | 10-counter scaffold |
| `_enrich_event` | `BPMXMixin → AStarLookup → AStar` | chained via `super()` |

The `_enrich_event` chain runs in MRO order: BPMXMixin first
calls `super()._enrich_event(event)` which routes to
AStarLookup → AStar (h, f, is_cached, is_bounded, propagate
casts), then BPMXMixin adds its `pathmax_apply` / `bpmx_lift`
/ `bpmx_forward` int-casts.

## Counters

10-counter scaffold (inherited from `BPMXMixin`):

```
pathmax (2):
  cnt_pathmax_attempts     -- expansions where rule_pathmax fired
  cnt_pathmax_lifts        -- successful tightenings

bpmx (5):
  cnt_bpmx_attempts        -- expansions where BPMX cascade ran
  cnt_bpmx_iterations      -- total iteration rounds
  cnt_bpmx_rule3_lifts     -- Rule 3 (parent up) fires
  cnt_bpmx_rule1_forwards  -- Rule 1 (child down) fires
  cnt_bpmx_subtree_states  -- BFS subtree visits

frontier (3, mirrored from FrontierPriority on every read):
  cnt_push, cnt_pop, cnt_decrease
```

**Cache-hit interaction**: when a cached state is popped,
`_early_exit` fires BEFORE `_pre_expand`, so the BPMX cascade
does NOT run for that pop. cnt_bpmx_attempts therefore can be
strictly less than the count of non-goal pops when the cache
covers any expansion target.

## Recording event types

In addition to AStar's `push` / `pop` / `decrease_g`:

From AStarLookup:
- `propagate_wave`, `propagate` (pre-search; from
  `propagate_pathmax`).
- Event flags `is_cached` / `is_bounded` on push / pop.

From BPMXMixin:
- `pathmax_apply` (isolated rule fire).
- `bpmx_iteration` (cascade round-marker).
- `bpmx_lift` (Rule 3 fired during BPMX).
- `bpmx_forward` (Rule 1 fired during BPMX).

A cached state in the BPMX subtree is skipped from lift
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

| Method | Cache | rule_pathmax | depth_bpmx | Notes |
|---|:---:|:---:|:---:|---|
| `graph_abc_cached_at_b_off()` | yes | None | 0 | matches AStarLookup |
| `grid_4x4_bpmx_full_no_cache()` | no | None | None | matches AStarBPMX |
| `grid_4x4_rule3_no_cache()` | no | 3 | 0 | matches AStarBPMX |
| `graph_abc_cached_at_b_bpmx_d1()` | yes | None | 1 | combined |
| `grid_4x4_cached_suffix_bpmx_d1()` | yes | None | 1 | cached-goal + BPMX |
| `graph_diamond_inconsistent_bpmx_full()` | no | None | None | inconsistent toy |

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
