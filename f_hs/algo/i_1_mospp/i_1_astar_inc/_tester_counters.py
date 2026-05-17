"""
============================================================================
 AStarIncMOSPP — counter pins on the canonical incremental-MOSPP
 fixture `grid_6x6_zigzag_mospp` (starts (0,0) / (2,3) / (0,3);
 goal (5,0); per-start optimal costs 15 / 10 / 12; Manhattan h
 to the fixed goal).

 One test method per param config (18 total): 1 cache (Group A),
 4 propagation depths (Group B), 13 BPMX rule x depth (Group C).
 Each pins the full non-memory counter dict. Values are the
 Phase-0b oracle output
 (`study/oracle.py` -> all 18 tuples distinct). Pins are
 RECORDING-OFF (matching the OMSPP / AStarRepMOSPP convention —
 no enrichment h-calls).

 Group C uses `carry_cache=True`: the sub-search-1 on-path
 cache is BPMX's inconsistency engine on the otherwise-
 consistent Manhattan h (see i_3_astar_bpmx/CLAUDE.md). Without
 it Rules 1/3 never lift and rule_1_depth_1 == rule_3_depth_1.
============================================================================
"""

from f_hs.algo.i_1_mospp.i_1_astar_inc import AStarIncMOSPP
from f_hs.problem.i_1_grid import ProblemGrid


def _run(**kwargs) -> AStarIncMOSPP:
    """
    ========================================================================
     Build + run AStarIncMOSPP on the canonical fixture
     (recording off) and return the algo for counter
     inspection.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_6x6_zigzag_mospp()
    algo = AStarIncMOSPP(problem=p,
                         h=lambda s, g: float(s.distance(g)),
                         **kwargs)
    algo.run()
    return algo


def _counters(algo: AStarIncMOSPP) -> dict:
    """
    ========================================================================
     Non-memory counter dict (mem_* dropped — size-dependent).
    ========================================================================
    """
    return {k: v for k, v in algo.counters.items()
            if not k.startswith('mem_')}



def test_only_cache() -> None:
    """
    ========================================================================
     Pin counters for config `only_cache`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx=None).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx=None)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 0,
        'cnt_bpmx_depth': 0,
        'cnt_bpmx_successes': 0,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 25,
        'cnt_generated': 36,
        'cnt_h_search': 33,
        'cnt_pop': 28,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 36,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_propagate_depth_1() -> None:
    """
    ========================================================================
     Pin counters for config `only_propagate_depth_1`
     (carry_cache=True, carry_bounds=False, propagate=True, propagate_depth=1, rule_bpmx=None).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=True, propagate_depth=1, rule_bpmx=None)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 0,
        'cnt_bpmx_depth': 0,
        'cnt_bpmx_successes': 0,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 24,
        'cnt_generated': 35,
        'cnt_h_search': 65,
        'cnt_pop': 27,
        'cnt_prop_attempts': 16,
        'cnt_prop_lifts': 2,
        'cnt_prop_waves': 1,
        'cnt_push': 35,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_propagate_depth_2() -> None:
    """
    ========================================================================
     Pin counters for config `only_propagate_depth_2`
     (carry_cache=True, carry_bounds=False, propagate=True, propagate_depth=2, rule_bpmx=None).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=True, propagate_depth=2, rule_bpmx=None)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 0,
        'cnt_bpmx_depth': 0,
        'cnt_bpmx_successes': 0,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 23,
        'cnt_generated': 34,
        'cnt_h_search': 70,
        'cnt_pop': 26,
        'cnt_prop_attempts': 18,
        'cnt_prop_lifts': 4,
        'cnt_prop_waves': 2,
        'cnt_push': 34,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_propagate_depth_3() -> None:
    """
    ========================================================================
     Pin counters for config `only_propagate_depth_3`
     (carry_cache=True, carry_bounds=False, propagate=True, propagate_depth=3, rule_bpmx=None).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=True, propagate_depth=3, rule_bpmx=None)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 0,
        'cnt_bpmx_depth': 0,
        'cnt_bpmx_successes': 0,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 23,
        'cnt_generated': 34,
        'cnt_h_search': 76,
        'cnt_pop': 26,
        'cnt_prop_attempts': 20,
        'cnt_prop_lifts': 6,
        'cnt_prop_waves': 3,
        'cnt_push': 34,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_propagate_depth_inf() -> None:
    """
    ========================================================================
     Pin counters for config `only_propagate_depth_inf`
     (carry_cache=True, carry_bounds=False, propagate=True, propagate_depth=None, rule_bpmx=None).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=True, propagate_depth=None, rule_bpmx=None)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 0,
        'cnt_bpmx_depth': 0,
        'cnt_bpmx_successes': 0,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 23,
        'cnt_generated': 34,
        'cnt_h_search': 88,
        'cnt_pop': 26,
        'cnt_prop_attempts': 24,
        'cnt_prop_lifts': 8,
        'cnt_prop_waves': 5,
        'cnt_push': 34,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_1_depth_1() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_1_depth_1`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='1', depth_bpmx=1).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='1', depth_bpmx=1)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 25,
        'cnt_bpmx_depth': 0,
        'cnt_bpmx_successes': 0,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 25,
        'cnt_generated': 36,
        'cnt_h_search': 112,
        'cnt_pop': 28,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 36,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_1_depth_2() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_1_depth_2`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='1', depth_bpmx=2).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='1', depth_bpmx=2)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 25,
        'cnt_bpmx_depth': 0,
        'cnt_bpmx_successes': 0,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 25,
        'cnt_generated': 36,
        'cnt_h_search': 224,
        'cnt_pop': 28,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 36,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_1_depth_3() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_1_depth_3`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='1', depth_bpmx=3).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='1', depth_bpmx=3)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 25,
        'cnt_bpmx_depth': 0,
        'cnt_bpmx_successes': 0,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 25,
        'cnt_generated': 36,
        'cnt_h_search': 338,
        'cnt_pop': 28,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 36,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_1_depth_inf() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_1_depth_inf`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='1', depth_bpmx=None).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='1', depth_bpmx=None)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 25,
        'cnt_bpmx_depth': 0,
        'cnt_bpmx_successes': 0,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 25,
        'cnt_generated': 36,
        'cnt_h_search': 1147,
        'cnt_pop': 28,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 36,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_2_depth_1() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_2_depth_1`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='2', depth_bpmx=1).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='2', depth_bpmx=1)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 25,
        'cnt_bpmx_depth': 0,
        'cnt_bpmx_successes': 6,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 25,
        'cnt_generated': 36,
        'cnt_h_search': 118,
        'cnt_pop': 28,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 36,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_3_depth_1() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_3_depth_1`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='3', depth_bpmx=1).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='3', depth_bpmx=1)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 25,
        'cnt_bpmx_depth': 0,
        'cnt_bpmx_successes': 1,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 25,
        'cnt_generated': 36,
        'cnt_h_search': 113,
        'cnt_pop': 28,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 36,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_3_depth_2() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_3_depth_2`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='3', depth_bpmx=2).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='3', depth_bpmx=2)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 24,
        'cnt_bpmx_depth': 1,
        'cnt_bpmx_successes': 4,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 24,
        'cnt_generated': 35,
        'cnt_h_search': 222,
        'cnt_pop': 27,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 35,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_3_depth_3() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_3_depth_3`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='3', depth_bpmx=3).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='3', depth_bpmx=3)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 23,
        'cnt_bpmx_depth': 2,
        'cnt_bpmx_successes': 4,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 23,
        'cnt_generated': 34,
        'cnt_h_search': 318,
        'cnt_pop': 26,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 34,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_3_depth_inf() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_3_depth_inf`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='3', depth_bpmx=None).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='3', depth_bpmx=None)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 23,
        'cnt_bpmx_depth': 2,
        'cnt_bpmx_successes': 4,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 23,
        'cnt_generated': 34,
        'cnt_h_search': 1035,
        'cnt_pop': 26,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 34,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_CASCADE_depth_1() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_CASCADE_depth_1`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='CASCADE', depth_bpmx=1).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='CASCADE', depth_bpmx=1)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 25,
        'cnt_bpmx_depth': 1,
        'cnt_bpmx_successes': 2,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 25,
        'cnt_generated': 36,
        'cnt_h_search': 197,
        'cnt_pop': 28,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 36,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_CASCADE_depth_2() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_CASCADE_depth_2`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='CASCADE', depth_bpmx=2).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='CASCADE', depth_bpmx=2)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 24,
        'cnt_bpmx_depth': 2,
        'cnt_bpmx_successes': 4,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 24,
        'cnt_generated': 35,
        'cnt_h_search': 421,
        'cnt_pop': 27,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 35,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_CASCADE_depth_3() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_CASCADE_depth_3`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='CASCADE', depth_bpmx=3).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='CASCADE', depth_bpmx=3)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 23,
        'cnt_bpmx_depth': 2,
        'cnt_bpmx_successes': 4,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 23,
        'cnt_generated': 34,
        'cnt_h_search': 629,
        'cnt_pop': 26,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 34,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def test_only_bpmx_rule_CASCADE_depth_inf() -> None:
    """
    ========================================================================
     Pin counters for config `only_bpmx_rule_CASCADE_depth_inf`
     (carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='CASCADE', depth_bpmx=None).
    ========================================================================
    """
    algo = _run(carry_cache=True, carry_bounds=False, propagate=False, propagate_depth=None, rule_bpmx='CASCADE', depth_bpmx=None)
    assert _counters(algo) == {
        'cnt_bpmx_attempts': 23,
        'cnt_bpmx_depth': 2,
        'cnt_bpmx_successes': 4,
        'cnt_cache_hits_at_init': 1,
        'cnt_decrease': 0,
        'cnt_expanded': 23,
        'cnt_generated': 34,
        'cnt_h_search': 2148,
        'cnt_pop': 26,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_prop_waves': 0,
        'cnt_push': 34,
    }
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in algo.solutions.items()}
    assert costs == {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}
