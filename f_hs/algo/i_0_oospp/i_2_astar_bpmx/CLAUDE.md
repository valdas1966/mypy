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
    rule_bpmx: str | None = None,
    depth_bpmx: int | None = 1,
)
```

Single-axis mechanism API: `rule_bpmx` selects what runs,
`depth_bpmx` controls how far it walks.

#### `rule_bpmx ∈ {None, '1', '2', '3', 'CASCADE'}`

| Value | Behavior |
|---|---|
| `None` | mechanism off (default; ≡ plain AStar) |
| `'1'` | Rule 1 (Mero parent→child) — top-down sweep, no iteration |
| `'2'` | Rule 2 (Felner min-children→parent) — depth-1 only by structural constraint |
| `'3'` | Rule 3 (Felner strongest child→parent) — bottom-up sweep, no iteration |
| `'CASCADE'` | Felner Algorithm 2 — Rules 1 + 3 alternating, iterated to fixed point |

#### `depth_bpmx ∈ {None, int >= 1}`

BFS-subtree depth from the popped state. Default `1` (immediate
parent-children neighborhood). `None` ⇒ full reachable subtree
(visited-set bounded). For Rule 2, `depth_bpmx` must be `1` —
the operator has no chained-grandparent analogue.

### Storage (HBounded auto-wrap)

Lifted h-values persist via an `HBounded` layer in the heuristic
chain. Auto-wraps an empty `HBounded` when `bounds=None` AND `h`
is a callable AND `rule_bpmx is not None`. Bounds are admissible
by construction (triangle inequality), preserving A* optimality.

### Frontier staleness

A lift on a state already in the frontier with its old priority
is left as-is. A* with inconsistent heuristics accepts stale
priorities (Martelli bound; Felner §4 analysis). Re-heaping is
not done. This matches Felner Algorithm 2's pragmatic choice.

### Validation (rejected configurations)

| Input | Error | Reason |
|---|---|---|
| `rule_bpmx not in {None, '1', '2', '3', 'CASCADE'}` | `ValueError` | enum |
| `depth_bpmx` not `None` and not `int >= 1` | `ValueError` | use `rule_bpmx=None` for off |
| `rule_bpmx == '2'` with `depth_bpmx != 1` | `ValueError` | Rule 2 cannot propagate beyond depth 1 |
| Pre-built `HBase` `h` containing `HCached` | `TypeError` | route to `AStarLookup` |
| Pre-built `HBase` `h` combined with `bounds` | `ValueError` | would double-wrap |
| Mechanism on but no `HBounded` reachable | `ValueError` | needs storage for lifts |

## Counters

12-name scaffold in four visual groups (returned via
`algo.counters`):

```
Counters(
  # bpmx mechanism (unified across all rule_bpmx values)
  cnt_bpmx_attempts    = N    # _pre_expand calls when rule_bpmx is set
  cnt_bpmx_successes   = N    # successful lifts (cumulative)
  cnt_bpmx_depth       = N    # max BFS-level at which a lift fired

  # frontier (mirrored from FrontierPriority)
  cnt_push             = N
  cnt_pop              = N
  cnt_decrease         = N

  # search-semantic (inherited from AlgoSPP)
  cnt_expanded         = N
  cnt_generated        = N

  # memory snapshot (post-run)
  mem_open             = N
  mem_closed           = N
  mem_cache            = N    # 0 — no HCached on AStarBPMX
  mem_bounds           = N
)
```

- **`cnt_bpmx_attempts`** — incremented once per `_pre_expand`
  call when `rule_bpmx is not None`. Counts mechanism dispatches.
- **`cnt_bpmx_successes`** — incremented per successful lift,
  regardless of which rule fired. Sum across the run.
- **`cnt_bpmx_depth`** — **max tracker** (not cumulative).
  Tracks the deepest BFS-level (0 = root) at which any
  successful lift fired. Updated via `assign` on each lift;
  stays at 0 if no lifts fire (or if Rule 2 lifts only the
  root). Divided into informativeness regimes by rule:
   - Rule '1' deep — lifts at levels [1, depth_bpmx]; max informative.
   - Rule '3' deep — lifts at levels [0, depth_bpmx − 1]; max informative.
   - Rule '2' (depth=1 only) — lifts at level 0; max stays 0.
   - CASCADE — lifts at any level [0, depth_bpmx]; max informative.

Per-rule lift breakdown remains visible via `bpmx_lift` /
`bpmx_forward` / `pathmax_apply` recording events for
diagnostic runs.

Heap-op counters are mirrored from the frontier on each
property access via `Counters.assign` — single source of truth

Heap-op counters are mirrored from the frontier on each
property access via `Counters.assign` — single source of truth
is `FrontierPriority`.

## Recording — event schema

In addition to AStar's `push` / `pop` / `decrease_g`:

### `pathmax_apply` (Rule 2 only)
```
{type, state, rule=2, h_old, h_new, via_children, duration}
```
Emitted on successful Rule 2 lifts (depth-1 only). `state`
is the lifted parent; `via_children` is a tuple of all its
immediate children.

### `bpmx_lift` (Rule 3 — alone or in CASCADE)
```
{type: 'bpmx_lift', state, h_old, h_new, via_child, duration}
```
`state` is the lifted parent; `via_child` is the strongest
child that produced the lift.

### `bpmx_forward` (Rule 1 — alone or in CASCADE)
```
{type: 'bpmx_forward', state, h_old, h_new, via_parent,
 duration}
```
`state` is the lifted child; `via_parent` is the parent that
pushed the lifted h down.

### `bpmx_iteration` (CASCADE only)
```
{type: 'bpmx_iteration', state, iteration, num_levels,
 num_states, duration}
```
State-tagged meta-event marking the start of each fixed-point
iteration of the cascade. `state` is the popped (root) node;
`iteration` resets to 1 at the start of each expansion's
cascade and increments per round; `num_levels` is the BFS
depth, `num_states` is the total subtree size. Isolated rule
sweeps (`rule_bpmx in {'1', '2', '3'}`) emit no iteration
events — they run a single non-iterated pass.

`h_old` and `h_new` are int-cast on enrichment for all four
event types.

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

| Method | Notes |
|---|---|
| `grid_4x4(rule_pathmax=None, depth_bpmx=0)` | Parametric on the canonical 4x4 obstacle grid with Manhattan h. Defaults reproduce off-mode (≡ plain AStar). All ablation corners and mixed configurations are reached via kwargs (e.g. `grid_4x4(rule_pathmax=2)`, `grid_4x4(depth_bpmx=None)`, `grid_4x4(rule_pathmax=3, depth_bpmx=1)`). |
| `graph_diamond_inconsistent_bpmx_full()` | Inconsistent toy graph (`B` has h=4) + BPMX(∞), `is_recording=True` — verifies lift events fire. |

## Tests

Three tester files, with a clear partitioning rule:

| File | Scope |
|---|---|
| `_tester.py` | Everything that isn't grid_4x4_obstacle per-rule recording or counter pinning: validation, off-mode, optimality across (rule × depth), inconsistent-diamond lifts, generic event-schema tests on toy graphs, generic counter invariants (scaffold shape, off-mode, attempts-per-expansion, subtree bound), subclass / factory. |
| `_tester_recording.py` | One method per Felner rule (None, 1, 2, 3) on `grid_4x4_obstacle`. Each is a FULL event-stream pin (single `actual == expected` assertion against the normalized event list, `duration` stripped). Rule None tests `depth_bpmx=None`; rules 1 / 2 / 3 test `depth_bpmx=0`. |
| `_tester_counters.py` | One method per Felner rule (None, 1, 2, 3) on `grid_4x4_obstacle` with `depth_bpmx=None`. Each pins the full counter dict (10 mechanism/frontier names; mem_* stripped). |

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
- `f_core.counters.Counters` (14-name scaffold (10 mechanism/frontier + 4 memory))
