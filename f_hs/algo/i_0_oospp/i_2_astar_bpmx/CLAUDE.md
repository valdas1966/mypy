# AStarBPMX

## Purpose

A* with **Felner's Pathmax Rules and BPMX** (Bidirectional
Pathmax) for inconsistent heuristics. Faithful to Felner et al.,
*Inconsistent Heuristics in Theory and Practice*, AIJ 2011.

Standalone sibling of `AStarLookup`. Both classes extend `AStar`
and live in `i_2_*/` — neither depends on the other. `AStarLookup`
owns cache-driven lookup features (HCached early-term,
suffix-stitching, `to_cache` harvest, `propagate_pathmax`).
`AStarBPMX` owns the in-search Felner pathmax rules and the
BPMX(d) cascade.

The shared in-search mechanism is implemented in
`f_hs/algo/i_0_oospp/mixins/bpmx/main.py` (`BPMXMixin`). `AStarBPMX` is a
thin wrapper that composes the mixin with vanilla `AStar`
(MRO: AStarBPMX → BPMXMixin → AStar → AlgoSPP). The combined
class with cache + BPMX is `AStarLookupBPMX`
(`i_3_astar_lookup_bpmx/`).

## Felner Numbering — locked

| Rule | Direction | Formula |
|---|---|---|
| **Rule 1** (Mero, 1984) | parent → child | `h'(c) = max(h(c), h(p) - w(p, c))` |
| **Rule 2** (Felner) | children → parent via min | `h'(p) = max(h(p), min_i(h(c_i) + w(p, c_i)))` |
| **Rule 3** (Felner) | single child → parent (reverse pathmax) | `h'(p) = max(h(p), max_c(h(c) - w(c, p)))` |
| **BPMX** | Rules 1 + 3 cascading, depth `d` | Felner Algorithm 2 |

This adheres to `Papers/Heuristic Search/Inconsistent
Heuristics/Inconsistent Heuristics.pdf` Sections 5.1–5.3 and the
refactored `2026/04/Reports/MOSPP.tex`. **Rule 2 (Felner)** —
children → parent via min — is included for completeness; Felner
notes its limited utility when Rules 1 and 3 are both used
(Felner §5.4.1).

## Public API

### Constructor

```python
AStarBPMX(
    problem: ProblemSPP[State],
    h: HBase[State] | Callable[[State], int] | None = None,
    name: str = 'AStarBPMX',
    is_recording: bool = False,
    search_state: SearchStateSPP[State] | None = None,
    bounds: dict[State, float] | None = None,
    rule_pathmax: int | None = None,
    depth_bpmx: int | None = 0,
)
```

Two orthogonal mechanisms:

#### `rule_pathmax` — isolated Felner rule, **depth 1 only**

| Value | Meaning |
|---|---|
| `None` | no isolated pathmax rule (default) |
| `1` | Rule 1 (Mero parent→child) |
| `2` | Rule 2 (Felner min-children→parent) |
| `3` | Rule 3 (Felner single child→parent reverse) |

Applied **once per expansion** at the immediate parent-children
neighborhood. No cascading. Rule 1 lifts every child; Rule 2
lifts the parent from cost-weighted min over children; Rule 3
lifts the parent from the strongest child's reverse-pathmax
estimate.

#### `depth_bpmx` — BPMX(d) cascade depth (Felner Algorithm 2)

| Value | Meaning |
|---|---|
| `0` | BPMX off (default) |
| `n >= 1` | cascade up to `n` levels deep |
| `None` | cascade through full reachable subtree (visited-set bounded) |

BPMX is the cascading combination of **Rules 1 + 3** propagated
outward through the d-level successor subtree of the expanded
node, **iterated to a fixed point**. BFS-spans the subtree from
the popped node, then alternately applies Rule 3 bottom-up
(parents lift from strongest child) and Rule 1 top-down (parents
push to children). Self-amortizes via no-improvement
short-circuit.

### Independence and redundancy

The two knobs are independent. With both on:
- Isolated rule fires once at the immediate parent-children
  level.
- BPMX cascade additionally propagates Rules 1 + 3 outward.

If `rule_pathmax in {1, 3}` and BPMX is on, the chosen rule
fires twice within one expansion (once isolated, once inside
BPMX) — redundant but correct (BPMX is idempotent; the second
application tightens nothing).

### Storage (HBounded auto-wrap)

Lifted h-values persist via an `HBounded` layer in the heuristic
chain. Auto-wraps an empty `HBounded` when `bounds=None` AND `h`
is a callable AND a mechanism is enabled. Bounds are admissible
by construction (triangle inequality), preserving A* optimality.

### Frontier staleness

A lift on a state already in the frontier with its old priority
is left as-is. A* with inconsistent heuristics accepts stale
priorities (Martelli bound; Felner §4 analysis). Re-heaping is
not done. This matches Felner Algorithm 2's pragmatic choice.

### Validation (rejected configurations)

| Input | Error | Reason |
|---|---|---|
| `rule_pathmax not in {None, 1, 2, 3}` | `ValueError` | Felner numbering only |
| `depth_bpmx` not `None` and not `int >= 0` | `ValueError` | guard against typos / bool |
| Pre-built `HBase` `h` containing `HCached` | `TypeError` | route to `AStarLookup` |
| Pre-built `HBase` `h` combined with `bounds` | `ValueError` | would double-wrap |
| Mechanism on but no `HBounded` reachable | `ValueError` | needs storage for lifts |

## Counters

10-counter scaffold in three visual groups (returned via
`algo.counters`):

```
Counters(
  cnt_pathmax_attempts    = N    # times rule_pathmax pass ran
  cnt_pathmax_lifts       = N    # successful tightenings

  cnt_bpmx_attempts       = N    # times BPMX cascade triggered
  cnt_bpmx_iterations     = N    # total iteration rounds
  cnt_bpmx_rule3_lifts    = N    # Rule 3 fires (parent up)
  cnt_bpmx_rule1_forwards = N    # Rule 1 fires (child down)
  cnt_bpmx_subtree_states = N    # states in BFS subtrees

  cnt_push                = N    # frontier push (mirrored)
  cnt_pop                 = N    # frontier pop (mirrored)
  cnt_decrease            = N    # frontier decrease (mirrored)
)
```

Heap-op counters are mirrored from the frontier on each
property access via `Counters.assign` — single source of truth
is `FrontierPriority`.

## Recording — event schema

In addition to AStar's `push` / `pop` / `decrease_g`:

### `pathmax_apply`
```
{type, state, rule, h_old, h_new, ..., duration}
```
Emitted on **successful** isolated-rule lifts (no event on a
no-op attempt).

| Rule | `state` is | Extra fields |
|---|---|---|
| 1 | the lifted child | `via_parent` |
| 2 | the lifted parent | `via_children` (tuple of children) |
| 3 | the lifted parent | `via_child` (the strongest child) |

`h_old` and `h_new` are int-cast on enrichment.

### `bpmx_iteration`
```
{type: 'bpmx_iteration', state, iteration, num_levels,
 num_states, duration}
```
State-tagged meta-event marking the start of each iteration of
the BPMX cascade. `state` is the popped (root) node;
`iteration` resets to 1 at the start of each expansion's
cascade and increments per round; `num_levels` is the BFS depth
(in the cascade), `num_states` is the total subtree size.

### `bpmx_lift` (Rule 3 fired during BPMX)
```
{type: 'bpmx_lift', state, h_old, h_new, via_child, duration}
```

### `bpmx_forward` (Rule 1 fired during BPMX)
```
{type: 'bpmx_forward', state, h_old, h_new, via_parent,
 duration}
```

`h_old` / `h_new` int-cast on enrichment.

## Inheritance

```
AlgoSPP[State]
  └── AStar[State]
        ├── AStarLookup[State]   (cache + bounds + propagate_pathmax)
        └── AStarBPMX[State]     (this class — Felner pathmax + BPMX)
```

`AStarLookup` and `AStarBPMX` are **siblings**, not in a chain.
`AStar`'s strict `type(self) is AStar` HCached/HBounded check
is bypassed for both subclasses.

## Out of scope (lives on AStarLookup or AStarLookupBPMX)

- HCached early-termination, suffix-stitching, `to_cache`
  harvest — live on `AStarLookup`.
- Pre-search `propagate_pathmax` from cached seeds — lives on
  `AStarLookup`.
- Cache + bounds + BPMX in one pass — live on
  `AStarLookupBPMX` (`i_3_astar_lookup_bpmx/`). That class
  composes `BPMXMixin` with `AStarLookup` and is what
  `k×A*-CB` uses for MOSPP / OMSPP sub-search.

## Factory

| Method | `rule_pathmax` | `depth_bpmx` | Notes |
|---|---:|---:|---|
| `grid_4x4_off()` | None | 0 | baseline (≡ plain AStar) |
| `grid_4x4_rule1()` | 1 | 0 | Felner Rule 1 only |
| `grid_4x4_rule2()` | 2 | 0 | Felner Rule 2 only |
| `grid_4x4_rule3()` | 3 | 0 | Felner Rule 3 only |
| `grid_4x4_bpmx_d1()` | None | 1 | BPMX(1) — classical Felner |
| `grid_4x4_bpmx_d2()` | None | 2 | BPMX(2) |
| `grid_4x4_bpmx_full()` | None | None | BPMX(∞) |
| `grid_4x4_rule3_bpmx_d1()` | 3 | 1 | combined (redundant Rule 3) |
| `graph_diamond_inconsistent_bpmx_full()` | None | None | inconsistent toy graph |

## Tests

Three tester files, with a clear partitioning rule:

| File | Scope |
|---|---|
| `_tester.py` | Everything that isn't grid_4x4_obstacle per-rule recording or counter pinning: validation, off-mode, optimality across (rule × depth), inconsistent-diamond lifts, generic event-schema tests on toy graphs, generic counter invariants (scaffold shape, off-mode, attempts-per-expansion, subtree bound), subclass / factory. |
| `_tester_recording.py` | One method per Felner rule (None, 1, 2, 3) on `grid_4x4_obstacle`. Each is a FULL event-stream pin (single `actual == expected` assertion against the normalized event list, `duration` stripped). Rule None tests `depth_bpmx=None`; rules 1 / 2 / 3 test `depth_bpmx=0`. |
| `_tester_counters.py` | One method per Felner rule (None, 1, 2, 3) on `grid_4x4_obstacle` with `depth_bpmx=None`. Each pins the full 10-counter dict. |

Pinned values exploit the consistent-h property of Manhattan
on the unit-cost grid: Rules 1 and 3 attempt but never lift;
Rule 2 fires twice at "local minimum" cells where the obstacle
forces a detour; the BPMX cascade itself tightens nothing.

## Dependencies

- `f_hs.algo.i_1_astar.AStar` (base)
- `f_hs.algo.i_0_base.AlgoSPP` (via AStar; contributes
  `_pre_expand` hook)
- `f_hs.heuristic.i_1_callable.HCallable`
- `f_hs.heuristic.i_1_bounded.HBounded` (storage for lifts)
- `f_hs.heuristic.i_1_cached.HCached` (rejection check only)
- `f_core.counters.Counters` (10-counter scaffold)
