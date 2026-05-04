# BPMXMixin — Felner Pathmax + BPMX(d) cascade

## Purpose

Reusable in-search mechanism for **Felner pathmax rules** and **BPMX(d) cascade** propagation, sourced from Felner et al., *"Inconsistent Heuristics in Theory and Practice"* (AIJ 2011).

Consumed by exactly two OOSPP algorithm classes:

- `AStarBPMX` — vanilla A* + BPMX (`AStarBPMX → BPMXMixin → AStar → AlgoSPP`).
- `AStarLookupBPMX` — cache + bounds + propagate_pathmax + in-search BPMX in one pass (`AStarLookupBPMX → BPMXMixin → AStarLookup → AStar`).

## Why it lives here (and not at `f_hs/algo/`)

BPMX as implemented operates on a **per-search-tree A*** — the parent/children pathmax mechanics assume a single-source single-goal search. Even when an OMSPP / MOSPP orchestrator composes a BPMX-flavored sub-algo via the `_inner_algo_cls` hook on `KAStarInc`, the BPMX mechanism still runs *inside the OOSPP sub-search*. A multi-goal-aware BPMX variant (e.g., aggregate-Φ pathmax) would be a different mixin with different math, not a reuse of this one.

So BPMX is intrinsically OOSPP-scoped. The original "kept at algo/ parent for symmetric reuse across omspp/mospp" rationale didn't materialize and overstated the abstraction.

## Two orthogonal mechanisms

The host class accepts two independent kwargs:

### `rule_pathmax ∈ {None, 1, 2, 3}`

Isolated Felner rule applied once per expansion at the immediate parent → children neighborhood (depth 1 only). Felner numbering:

| rule | direction | formula |
|:---:|---|---|
| 1 | parent → child (Mero, 1984) | `h'(c) = max(h(c), h(p) − w(p, c))` |
| 2 | children → parent (min) | `h'(p) = max(h(p), min_i(h(c_i) + w(p, c_i)))` |
| 3 | child → parent (reverse pathmax) | `h'(p) = max(h(p), h(c) − w(p, c))` |

### `depth_bpmx ∈ {None, 0, 1, 2, ...}`

BPMX(d) cascade — recursive propagation up to depth `d` along the search tree. `depth_bpmx=0` is a no-op (pure pathmax); `depth_bpmx=None` disables the cascade.

The two kwargs compose: a host can use rules-only, BPMX-only, or both.

## MRO contract

Place `BPMXMixin` BEFORE `AStar` / `AStarLookup` in the host's bases tuple so `super()` chains resolve mixin overrides first:

```python
class AStarBPMX(BPMXMixin, AStar[State], Generic[State]):
    ...

class AStarLookupBPMX(BPMXMixin, AStarLookup[State], Generic[State]):
    ...
```

## Counters (10 total — overrides AlgoSPP's 3-counter `counters`)

| group | counters |
|---|---|
| pathmax (2) | `cnt_pathmax_apply`, `cnt_pathmax_lift` |
| bpmx (5) | `cnt_bpmx_visit`, `cnt_bpmx_lift`, `cnt_bpmx_skip_*` |
| frontier (3) | `cnt_push`, `cnt_pop`, `cnt_decrease` (mirrored from `FrontierPriority`) |

## Validation hooks

Static helpers exposed for host classes to call from `__init__`:

- `BPMXMixin._validate_rule_pathmax(value)` — raises `ValueError` on bad input.
- `BPMXMixin._validate_depth_bpmx(value)` — same.
- `BPMXMixin._chain_contains_hcached(h)` — chain inspection helper.
- `BPMXMixin._find_hbounded(chain)` — chain inspection helper.

## Dependencies

- `f_core.counters.Counters` — 10-counter scaffold.
- `f_hs.heuristic.{HBase, HCached, HBounded}` — chain-walk helpers.

## Tests

No standalone tester for this mixin — tests live with the consumers:

- `oospp/i_2_astar_bpmx/_tester.py`
- `oospp/i_3_astar_lookup_bpmx/_tester.py` (incl. MRO test)
