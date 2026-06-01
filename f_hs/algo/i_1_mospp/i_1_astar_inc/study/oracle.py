"""
============================================================================
 Oracle for AStarIncMOSPP on `grid_6x6_zigzag_mospp`.

 Runs all 22 configs (1 cache + 4 propagation + 13 BPMX
 + 4 propagate-then-bpmx combined),
 dumps the non-memory counter tuple per config, and reports
 any duplicate tuples (= configs that collapsed). Phase 0b of
 the AStarIncMOSPP plan — the input to pinning
 `_tester_counters.py` / `_tester_recording.py`.

 Run:
   python -m f_hs.algo.i_1_mospp.i_1_astar_inc.study.oracle
============================================================================
"""
from collections import defaultdict

from f_hs.algo.i_1_mospp.i_1_astar_inc import AStarIncMOSPP
from f_hs.problem.i_1_grid import ProblemGrid


# 22 configs: 1 cache + 4 propagation + 13 BPMX
# + 4 propagate-then-bpmx combined (Group D).
CONFIGS: list[tuple[str, dict]] = [
    # Group A — only cache.
    ('only_cache',
     dict(carry_cache=True, adaptive_h=False,
          propagate=False, propagate_depth=None,
          rule_bpmx=None)),

    # Group B — only propagation (depths 1, 2, 3, inf).
    *[(f'only_propagate_depth_{d if d is not None else "inf"}',
       dict(carry_cache=True, adaptive_h=False,
            propagate=True, propagate_depth=d,
            rule_bpmx=None))
      for d in [1, 2, 3, None]],

    # Group C — only BPMX (rule x depth). `carry_cache=True`
    # is required: the sub-search-1 on-path cache injects the
    # perfect-h beacons that create local inconsistency for
    # the in-search Felner cascade. On consistent Manhattan h
    # with no cache, Rules 1/3 never lift and
    # rule_1_depth_1 == rule_3_depth_1 (documented BPMX
    # inconsistency-engine requirement — see
    # i_3_astar_bpmx/CLAUDE.md). propagate / adaptive_h stay
    # off so the BPMX axis is isolated.
    *[(f'only_bpmx_rule_{r}_depth_'
       f'{d if d is not None else "inf"}',
       dict(carry_cache=True, adaptive_h=False,
            propagate=False, propagate_depth=None,
            rule_bpmx=r, depth_bpmx=d))
      for r, d in [
          ('1', 1), ('1', 2), ('1', 3), ('1', None),
          ('2', 1),
          ('3', 1), ('3', 2), ('3', 3), ('3', None),
          ('CASCADE', 1), ('CASCADE', 2),
          ('CASCADE', 3), ('CASCADE', None),
      ]],

    # Group D — propagate THEN bpmx (the combined quadrant;
    # both write the shared HBounded layer via max-combine).
    # On this fixture there is no expansion synergy — the grid
    # saturates at 23 and convergent propagation SUBSUMES BPMX
    # (see `prop_inf_bpmx_rule_3_depth_3`: rule_3_depth_3 lifts
    # 4 alone but 0 once propagation has converged). These rows
    # exist for combined-path coverage, the subsumption canary,
    # and the decision-guide fact (prefer propagation; reach
    # for BPMX only when uncached / depth-capped). Optimality
    # is preserved (admissible composition).
    ('prop_1_bpmx_rule_CASCADE_depth_1',
     dict(carry_cache=True, adaptive_h=False,
          propagate=True, propagate_depth=1,
          rule_bpmx='CASCADE', depth_bpmx=1)),
    ('prop_2_bpmx_rule_3_depth_2',
     dict(carry_cache=True, adaptive_h=False,
          propagate=True, propagate_depth=2,
          rule_bpmx='3', depth_bpmx=2)),
    ('prop_2_bpmx_rule_CASCADE_depth_2',
     dict(carry_cache=True, adaptive_h=False,
          propagate=True, propagate_depth=2,
          rule_bpmx='CASCADE', depth_bpmx=2)),
    ('prop_inf_bpmx_rule_3_depth_3',
     dict(carry_cache=True, adaptive_h=False,
          propagate=True, propagate_depth=None,
          rule_bpmx='3', depth_bpmx=3)),
]


def _counters(algo: AStarIncMOSPP) -> dict[str, int]:
    """
    ========================================================================
     Non-memory counter dict (mem_* dropped — size-dependent).
    ========================================================================
    """
    return {k: v for k, v in algo.counters.items()
            if not k.startswith('mem_')}


def main() -> None:
    """
    ========================================================================
     Run every config, print the counter table, report
     collisions and per-start costs.
    ========================================================================
    """
    rows: list[tuple[str, dict]] = []
    tuples_to_configs: dict[tuple, list[str]] = defaultdict(list)
    costs_seen: set = set()

    for name, kwargs in CONFIGS:
        p = ProblemGrid.Factory.grid_6x6_zigzag_mospp()
        algo = AStarIncMOSPP(
            problem=p,
            h=lambda s, g: float(s.distance(g)),
            is_recording=False,
            **kwargs,
        )
        sol = algo.run()
        counters = _counters(algo)
        tup = tuple(sorted(counters.items()))
        rows.append((name, counters))
        tuples_to_configs[tup].append(name)
        costs = tuple(sorted(
            (s.key.row, s.key.col, v.cost)
            for s, v in sol.per_start.items()))
        costs_seen.add(costs)

    keys = sorted({k for _, c in rows for k in c})
    print(f"{'config':36} " +
          " ".join(f"{k:>13}" for k in keys))
    for name, counters in rows:
        print(f"{name:36} " +
              " ".join(f"{counters.get(k, 0):>13}"
                       for k in keys))

    print()
    if len(costs_seen) == 1:
        print(f"Per-start costs (all configs equal): "
              f"{sorted(costs_seen)[0]}")
    else:
        print(f"!! per-start costs DIFFER across configs: "
              f"{costs_seen}")

    print()
    collisions = {t: cs for t, cs in tuples_to_configs.items()
                  if len(cs) > 1}
    if collisions:
        print(f"COLLISIONS: {len(collisions)} set(s), "
              f"{len(CONFIGS)} configs total")
        for _, cs in collisions.items():
            print(f"  {cs}")
    else:
        print(f"All {len(CONFIGS)} tuples distinct. OK")


if __name__ == '__main__':
    main()
