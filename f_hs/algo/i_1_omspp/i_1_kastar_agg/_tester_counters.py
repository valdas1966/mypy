"""
============================================================================
 KAStarAgg — counter pin on the canonical OMSPP problem
 (`grid_4x4_obstacle_omspp`: start (0,0), goals (0,3) / (3,0)
 / (3,3); per-goal optimal costs 7 / 3 / 6; Manhattan h to
 each goal).

 KAStarAgg expands states by aggregated f over the k goals.
 The aggregator (MIN / MAX / AVG / RND / PROJECTION) shapes
 the search trace and counter values. Pin is for **MIN**
 (the canonical aggregator); other aggregators are exercised
 in `_tester.py`'s aggregation-specific scenarios.
============================================================================
"""

from f_hs.algo.i_1_omspp.i_1_kastar_agg import KAStarAgg
from f_hs.problem.i_1_grid import ProblemGrid


def test_counters_canonical_omspp_min() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters on the canonical OMSPP
     problem. 16 push / 16 pop / 2 decrease_g; 2 stale-pops
     when `cnt_h_update` re-tightens a frontier state's
     priority via the lazy refresh path.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KAStarAgg(problem=p,
                     h=lambda s, g: float(s.distance(g)),
                     agg='MIN')
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_h_search': 34,
        'cnt_h_update': 31,
        'cnt_phi_search': 16,
        'cnt_phi_update': 16,
        'cnt_push': 16,
        'cnt_pop': 16,
        'cnt_pop_stale': 2,
        'cnt_decrease': 2,
        'cnt_expanded': 14,
        'cnt_generated': 14,
    }


def test_per_goal_costs_canonical_omspp_min() -> None:
    """
    ========================================================================
     Pin per-goal optimal costs (KAStarAgg-MIN) on the
     canonical OMSPP problem: (0,3)=7, (3,0)=3, (3,3)=6.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KAStarAgg(problem=p,
                     h=lambda s, g: float(s.distance(g)),
                     agg='MIN')
    sol = algo.run()
    costs = {(g.key.row, g.key.col): s.cost
             for g, s in sol.per_goal.items()}
    assert costs == {(0, 3): 7, (3, 0): 3, (3, 3): 6}
