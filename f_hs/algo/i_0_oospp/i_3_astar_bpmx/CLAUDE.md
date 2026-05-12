# AStarBPMX

## Purpose

`AStarLookup` + in-search Felner pathmax / BPMX(d). Extends
`AStarLookup` with the per-expansion pathmax cascade
(`BPMXMixin`); inherits all cache, bounds,
`propagate_pathmax`, and `to_cache` machinery unchanged.

This is the canonical advanced-A* class for inconsistent /
asymmetric heuristics. Used by k×A*-CB-style sub-search when
BPMX is desired (set `_inner_algo_cls=AStarBPMX` on the
orchestrator).

## When to use AStarBPMX vs AStarLookup

| Need | Class |
|------|-------|
| Cache-hit early-term (HCached) | `AStarLookup` |
| Admissible bounds (HBounded) | `AStarLookup` |
| Pre-search pathmax (`propagate_pathmax`) | `AStarLookup` |
| Cache harvest (`to_cache`) | `AStarLookup` |
| In-search BPMX (Rules 1/2/3/CASCADE) | **`AStarBPMX`** |

If you don't need in-search BPMX, use `AStarLookup` — it's
smaller, faster, and has no BPMX hooks in its MRO.

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

All `AStarLookup` kwargs are accepted unchanged. Adds
`rule_bpmx` and `depth_bpmx`.

### BPMX semantics
- `rule_bpmx ∈ {None, '1', '2', '3', 'CASCADE'}` — selects
  the Felner rule (or cascade) that runs at each
  `_pre_expand`. `None` (default) ⇒ mechanism off; the
  instance behaves identically to a plain `AStarLookup`.
- `depth_bpmx ∈ {None, int >= 1}` — BFS-subtree depth for
  Rules 1 / 3 / CASCADE; Rule 2 is depth-1 only by structural
  constraint (constructor enforces `depth_bpmx == 1`).

### BPMX storage requirement
BPMX writes lifted h-values into an `HBounded` layer in the
heuristic chain. The constructor auto-wraps an empty
`bounds={}` when:
- `rule_bpmx is not None`, AND
- `h` is a callable / None, AND
- `bounds` is None.

With a pre-built `HBase` chain the host must already include
`HBounded` — the constructor verifies and raises `ValueError`
otherwise.

### Validation
- `rule_bpmx not in {None, '1', '2', '3', 'CASCADE'}` →
  `ValueError`.
- `depth_bpmx not in {None} ∪ {int >= 1}` → `ValueError`.
- `rule_bpmx == '2'` with `depth_bpmx != 1` → `ValueError`
  (Rule 2 cannot propagate beyond depth 1).
- `rule_bpmx is not None` but no `HBounded` reachable in the
  chain → `ValueError`.

All inherited `AStarLookup` validations (cache without goal,
HCached goal not in problem.goals, pre-built HBase combined
with cache/bounds dicts) still apply.

## MRO

```
AStarBPMX → BPMXMixin → AStarLookup → AStar → AlgoSPP → ...
```

`BPMXMixin` sits between `AStarBPMX` and `AStarLookup` so the
mixin's `_pre_expand`, `counters`, and `_enrich_event`
overrides resolve before `AStarLookup`'s. The `_enrich_event`
super-chain runs in MRO order: `BPMXMixin` int-casts BPMX
events → `AStarLookup` adds `is_cached` / `is_bounded` / int-
casts on propagate → `AStar` adds `h` / `f`.

## Counters

15-name scaffold (per-class `_COUNTER_NAMES` override).

| group | counters | source |
|---|---|---|
| propagate (3) | `cnt_prop_waves`, `cnt_prop_attempts`, `cnt_prop_lifts` | inherited from `AStarLookup`'s pre-search `propagate_pathmax` |
| bpmx (3) | `cnt_bpmx_attempts`, `cnt_bpmx_successes`, `cnt_bpmx_depth` | in-search BPMX dispatch (BPMXMixin) |
| frontier (3) | `cnt_push`, `cnt_pop`, `cnt_decrease` | `FrontierPriority` (mirrored on every read) |
| search (2) | `cnt_expanded`, `cnt_generated` | inherited from `AlgoSPP` |
| memory (4) | `mem_open`, `mem_closed`, `mem_cache`, `mem_bounds` | `_memory_snapshot()` (post-run) |

In off-mode (`rule_bpmx=None`), the bpmx group stays at zero
and the instance is behaviourally identical to an
`AStarLookup` with the same other kwargs.

## Factory

| Method | Description |
|--------|-------------|
| `graph_abc_cached_at_b(rule_bpmx, depth_bpmx, is_recording)` | Parametric — cache covering {B,C}; defaults reproduce off-mode |
| `grid_4x4(rule_bpmx, depth_bpmx)` | Parametric — canonical 4x4 grid, no cache; defaults reproduce plain AStarLookup |
| `grid_4x4_beacon(rule_bpmx, depth_bpmx, is_recording)` | **Cached beacon at (0,1) with h\*=6** (gap=4 vs Manhattan). Primary rule-axis fixture; counter signature pinned for all valid (rule, depth) combinations |
| `grid_6x6_zigzag_beacon(rule_bpmx, depth_bpmx, is_recording)` | **Cached beacon at (1,0) with h\*=14** (gap=10) on the new zigzag grid. Depth-axis fixture --- counters differentiate cleanly across depth=1, 2, 3, ∞ for Rules 1, 3, and CASCADE |
| `graph_diamond_inconsistent_cascade()` | Inconsistent diamond + CASCADE(∞), recording on |
| `grid_4x4_cached_suffix_cascade_d1()` | Goal-cached + CASCADE depth=1 |

All construct via the kwargs API
(`cache=`, `goal=`, `bounds=`, `rule_bpmx=`, `depth_bpmx=`).

## Tests

Auto-discovered by `TestRunner`'s `_tester*.py` pattern.

All tests use a **single fixture**:
`Factory.grid_4x4_beacon(rule_bpmx, depth_bpmx)` — the
canonical OOSPP problem (`grid_4x4_obstacle`) with a cached
beacon at (0,1) holding `h*=6` (gap=4 vs. Manhattan=2). The
beacon is the inconsistency engine — without it, Rules 1 /
3 / CASCADE never lift on consistent Manhattan h. Scope is
strictly "canonical OOSPP × different BPMX configs."

| File | Count | Scope |
|------|------:|-------|
| `_tester.py` | 14 | Parametric optimality across all valid (rule, depth) configs — cost stays 7 |
| `_tester_counters.py` | 14 | Parametric counter pin per (rule, depth) — full dict per row of the probed matrix |
| `_tester_recording.py` | 4 | Full event-stream pins for 4 representative configs (None, Rule 1 d=None, Rule 3 d=1, CASCADE d=None) |

**Dropped scope** (intentionally — see session 2026-05-13):

- `_tester_*_no_cache.py` — removed entirely. Inconsistency
  source was hand-crafted `h_inc` dicts on the toy
  `graph_diamond`. The beacon-on-canonical fixture supersedes
  this with a cleaner injection mechanism on a real grid.
- Validation tests (`rule_bpmx` / `depth_bpmx` / `cache` /
  pre-built-HBase argument parsing) — removed from the
  surviving files. They test constructor behavior, not
  "canonical OOSPP with BPMX configs."
- Toy-graph tests (`graph_abc`, `graph_diamond_inconsistent_cascade`,
  `graph_abc_cached_at_b`) — removed. The canonical OOSPP +
  beacon covers the relevant code paths.
- Feature tests (`to_cache` harvest after combined run,
  `propagate_pathmax` callability, suffix-stitched
  `reconstruct_path`, MRO / subclass / Factory plumbing
  invariants) — removed. Those live (or will live) in
  `i_2_astar_lookup/` where the features originate.

Lookup-only tests (`_tester_cached.py`, `_tester_bounded.py`,
`_tester_pathmax.py`, `_tester_recording.py`,
`_tester_counters.py`) live in `i_2_astar_lookup/`.

## Inheritance

```
AlgoSPP[State]
└── AStar[State]
    └── AStarLookup[State]                 (i_2_astar_lookup/)
        └── AStarBPMX[State]               (this class)
```

## Dependencies
- `f_hs.algo.i_0_oospp.i_2_astar_lookup.AStarLookup` (base).
- `f_hs.algo.i_0_oospp.mixins.bpmx.BPMXMixin` (composed).
- `f_hs.heuristic.{HBase, HCached, HBounded, HCallable,
  CacheEntry}` (chain assembly inherited from AStarLookup).
