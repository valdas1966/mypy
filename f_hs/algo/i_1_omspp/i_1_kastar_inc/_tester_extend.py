"""
============================================================================
 KAStarInc -- nested-extend counter equivalence on canonical OMSPP.

 Canonical OMSPP problem (`grid_4x4_obstacle_omspp`: start
 (0,0), goals (0,3) / (3,0) / (3,3); Manhattan h to the
 active goal).

 The nested-extend chain
 `run([g0]) -> extend([g1]) -> extend([g2])` must produce, at
 each stage, the same cumulative counters as a fresh kA*-INC
 run on the same prefix of goals -- the state-reuse
 equivalence invariant for KAStarInc.extend().
============================================================================
"""

from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc
from f_hs.problem.i_1_grid import ProblemGrid


def _h(s, g) -> float:
    return float(s.distance(g))


def _strip_mem(counters) -> dict:
    return {k: v for k, v in counters.items()
            if not k.startswith('mem_')}


def _fresh_counters(k: int) -> dict:
    """
    ========================================================================
     Run kA*-INC from scratch on the canonical OMSPP problem
     subsetted to its first `k` goals and return the non-mem
     counter dict.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    p._goals = p._goals[:k]
    algo = KAStarInc(problem=p, h=_h)
    algo.run()
    return _strip_mem(algo.counters)


def test_extend_nested_matches_fresh_runs() -> None:
    """
    ========================================================================
     run([g0]) -> extend([g1]) -> extend([g2]) on the canonical
     3-goal OMSPP problem. At each stage assert the cumulative
     KAStarInc counters equal those of a fresh run on the same
     prefix of goals (state reuse via extend is equivalent to
     running from scratch at the larger k).
    ========================================================================
    """
    # Targets -- 3 fresh kA*-INC runs at k = 1, 2, 3.
    target_k1 = _fresh_counters(k=1)
    target_k2 = _fresh_counters(k=2)
    target_k3 = _fresh_counters(k=3)

    # Nested -- start with goal 0, extend to goal 1, then to goal 2.
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    g1, g2 = p._goals[1], p._goals[2]
    p._goals = p._goals[:1]
    algo = KAStarInc(problem=p, h=_h)

    # Stage k=1.
    algo.run()
    assert _strip_mem(algo.counters) == target_k1

    # Stage k=2.
    algo.extend([g1])
    assert _strip_mem(algo.counters) == target_k2

    # Stage k=3.
    algo.extend([g2])
    assert _strip_mem(algo.counters) == target_k3
