# BPMXMixin — Felner Pathmax + BPMX cascade

## Purpose

Reusable in-search mechanism for **Felner pathmax rules** and the **BPMX cascade** (Felner Algorithm 2), sourced from Felner et al., *"Inconsistent Heuristics in Theory and Practice"* (AIJ 2011).

Consumed by exactly one OOSPP algorithm class:

- `AStarBPMX` — extends `AStarLookup` with in-search BPMX
  (`AStarBPMX → BPMXMixin → AStarLookup → AStar → AlgoSPP`).
  Used by k×A*-CB-style sub-search when BPMX is desired.

## Why it lives here (and not at `f_hs/algo/`)

BPMX as implemented operates on a **per-search-tree A*** — the parent/children pathmax mechanics assume a single-source single-goal search. Even when an OMSPP / MOSPP orchestrator composes a BPMX-flavored sub-algo via the `_inner_algo_cls` hook on `KAStarInc`, the BPMX mechanism still runs *inside the OOSPP sub-search*. A multi-goal-aware BPMX variant (e.g., aggregate-Φ pathmax) would be a different mixin with different math, not a reuse of this one.

So BPMX is intrinsically OOSPP-scoped.

## Single-axis API

The host class accepts two kwargs: `rule_bpmx` selects what runs, `depth_bpmx` controls how far it walks.

### `rule_bpmx ∈ {None, '1', '2', '3', 'CASCADE'}`

| value | behavior |
|---|---|
| `None` | Mechanism off (no _pre_expand work). |
| `'1'` | Rule 1 (Mero, 1984) — parent → child top-down sweep over the d-level BFS subtree, no iteration. `h'(c) = max(h(c), h(p) − w(p, c))`. |
| `'2'` | Rule 2 (Felner) — children → parent via min, **depth-1 only by structural constraint**. `h'(p) = max(h(p), min_i(h(c_i) + w(p, c_i)))`. Constructor enforces `depth_bpmx == 1`. |
| `'3'` | Rule 3 (Felner) — strongest child → parent bottom-up sweep over the d-level BFS subtree, no iteration. `h'(p) = max(h(p), max_c(h(c) − w(c, p)))`. |
| `'CASCADE'` | Felner Algorithm 2 — Rules 1 + 3 alternating sweeps, iterated to fixed point over the d-level BFS subtree. The bidirectional pathmax propagation that gives BPMX its name. |

### `depth_bpmx ∈ {None, int >= 1}`

BFS-subtree depth from the popped state. Default `1` (immediate neighborhood). `None` ⇒ full reachable subtree, visited-set bounded.

### Why Rule 2 is depth-1 only

Rule 2's operator consumes "a parent + its **full children set**" and aggregates via min. Chaining requires treating the lifted parent as a child of its grandparent — but Rule 2 expects to receive "a parent + complete children set" at each invocation, not "a single child". The grandparent's children set doesn't include the lifted parent's siblings, so the operation has no chained-grandparent analogue. Rule 2 + `depth_bpmx > 1` (or `None`) is rejected by `_validate_combination` with a clear error.

### Why deep Rule 1 / Rule 3 alone?

The cascade is strictly ≥ either single-direction sweep but does roughly 2× the work and iterates. Single-direction sweeps trade some lift coverage for cheaper per-expansion overhead — useful for ablation studies (see Felner 2011 §5.4).

## MRO contract

Place `BPMXMixin` BEFORE its lookup ancestor in the host's bases tuple so `super()` chains resolve mixin overrides first:

```python
class AStarBPMX(BPMXMixin, AStarLookup[State], Generic[State]):
    ...
```

## Counters

The mixin declares a 3-counter mechanism scaffold; the host class can override via a class-level `_COUNTER_NAMES` attribute (per-class override pattern). When the host doesn't override, the mixin's `_BPMX_COUNTER_NAMES` default is used.

| group | counters | source |
|---|---|---|
| bpmx (3) | `cnt_bpmx_attempts`, `cnt_bpmx_lifts`, `cnt_bpmx_depth` | mechanism dispatch + sweep functions |
| frontier (3) | `cnt_push`, `cnt_pop`, `cnt_decrease` | `FrontierPriority` (mirrored on every read) |
| search (2) | `cnt_expanded`, `cnt_generated` | inherited from AlgoSPP |
| memory (5) | `mem_open`, `mem_closed`, `mem_cache`, `mem_bounds`, `mem_total` | `_memory_snapshot()` (post-run); `mem_total = Σ mem_*` |

### Counter semantics

- **`cnt_bpmx_attempts`** — incremented once per `_pre_expand` call when `rule_bpmx is not None` (excludes cache-hit early-exits, which fire before `_pre_expand`). Cumulative across the run.
- **`cnt_bpmx_lifts`** — incremented per successful lift, regardless of which rule fired. Cumulative across the run. For Rule 1 and Rule 3 alone, this counts the rule's lifts; for Rule 2 it counts the parent lift; for CASCADE it sums all Rule 3 + Rule 1 lifts across iterations.
- **`cnt_bpmx_depth`** — **max tracker** (not cumulative). Tracks the deepest BFS-level (0 = root) at which any successful lift fired. Updated via `assign` on each successful lift; stays at 0 if no lifts fire OR if Rule 2 lifts only the root.

`AStarBPMX` overrides `_COUNTER_NAMES` to prepend a `propagate` group (`cnt_prop_waves`, `cnt_prop_attempts`, `cnt_prop_lifts`) — inherited from its `AStarLookup` parent's pre-search `propagate_pathmax`.

## Validation hooks

Static helpers exposed for host classes to call from `__init__`:

- `BPMXMixin._validate_rule_bpmx(value)` — raises `ValueError` on bad input.
- `BPMXMixin._validate_depth_bpmx(value)` — same; rejects 0 (use `rule_bpmx=None` for off).
- `BPMXMixin._validate_combination(rule_bpmx, depth_bpmx)` — enforces `rule_bpmx == '2' ⇒ depth_bpmx == 1`.
- `BPMXMixin._find_hbounded(chain)` — chain inspection helper.

## Recording events

| event | when | fields |
|---|---|---|
| `pathmax_apply{rule=2}` | Rule 2 lifts the parent (only Rule 2 emits this; depth-1 only) | `state`, `rule=2`, `h_old`, `h_new`, `via_children`, `duration` |
| `bpmx_lift` | Rule 3 lifts (alone or in cascade) | `state`, `h_old`, `h_new`, `via_child`, `duration` |
| `bpmx_forward` | Rule 1 pushes (alone or in cascade) | `state`, `h_old`, `h_new`, `via_parent`, `duration` |
| `bpmx_iteration` | CASCADE only — emitted at the start of each fixed-point iteration | `state`, `iteration`, `num_levels`, `num_states`, `duration` |

`h_old` / `h_new` are int-cast on enrichment for all four event types. Isolated Rules 1 / 3 sweeps emit no `bpmx_iteration` (they run a single non-iterated pass).

## Dependencies

- `f_core.counters.Counters` — counter scaffold.
- `f_hs.heuristic.{HBase, HCached, HBounded}` — chain-walk helpers.

## Tests

No standalone tester for this mixin — tests live with its only consumer:

- `oospp/i_3_astar_bpmx/_tester_bpmx*.py` and `_tester_*_bpmx_*.py` (covers BPMX standalone, cache + BPMX, counter pins, recording pins).
