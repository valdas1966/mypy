"""
============================================================================
 Recording tests for KAStarAgg — one test per (is_lazy × is_opt ×
 store_vector) configuration.

 Each of the 8 tests:
   1. Runs kA*_agg on the canonical `grid_4x4_obstacle` problem
      with Φ=MIN and k=2 goals (costs 7 and 6).
   2. Asserts the final solutions dict (Cor 2: identical across
      all 8 configs).
   3. Asserts the per-run counter snapshot.
   4. Pins the full normalized event stream as a golden reference.

 The 5 new event types — `h_calc`, `phi_calc`, `responsible_set`,
 `refresh_skip`, `pop_stale` — are designed to make every config
 distinguishable at the event level:
   - `is_lazy`       → `pop_stale` (lazy only) vs `update_frontier`
                       (eager only).
   - `is_opt`        → `responsible_set` and `refresh_skip` fire
                       only under opt.
   - `store_vector`  → `h_calc` events drop to 0 after each state's
                       first `_compute_F`.
============================================================================
"""

from f_hs.algo.omspp._utils import normalize
from f_hs.algo.omspp.i_1_kastar_agg import KAStarAgg
from f_hs.problem.i_1_grid import ProblemGrid


def _grid_4x4_obstacle_multigoal() -> ProblemGrid:
    """
    ========================================================================
     4x4 grid with wall cells at (0,2) and (1,2). Start (0,0),
     goals [(0,3), (3,3)]. Optimal costs 7 and 6.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    grid = p.grid
    p._goals = [p._states[grid[0][3]],
                p._states[grid[3][3]]]
    return p


def _manhattan_grid(s, g) -> int:
    return (abs(s.key.row - g.key.row)
            + abs(s.key.col - g.key.col))

def test_agg_recording_lazy1_opt0_vec0() -> None:
    """
    ========================================================================
     Recording test: lazy=True, opt=False, vec=False.
     Pins the full event stream + counter snapshot for kA*_agg
     on grid_4x4_obstacle (Φ=MIN, k=2).
    ========================================================================
    """
    p = _grid_4x4_obstacle_multigoal()
    algo = KAStarAgg(problem=p, h=_manhattan_grid,
                     agg='MIN',
                     is_lazy=True,
                     is_opt=False,
                     store_vector=False,
                     is_recording=True)
    sols = algo.run()
    by_rc = {(g.key.row, g.key.col): s.cost
             for g, s in sols.items()}
    assert by_rc == {(3, 3): 6, (0, 3): 7}
    assert algo.counters == {'cnt_h_search': 25, 'cnt_h_update': 21, 'cnt_phi_search': 13, 'cnt_phi_update': 13, 'cnt_push': 16, 'cnt_pop': 13, 'cnt_pop_stale': 3, 'cnt_decrease': 0}
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'h_calc', 'state': (0, 0), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 0), 'goal': (3, 3), 'value': 6, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (0, 0), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3, 'parent': None},
        {'type': 'h_calc', 'state': (0, 0), 'goal': (0, 3), 'value': 3, 'phase': 'update'},
        {'type': 'h_calc', 'state': (0, 0), 'goal': (3, 3), 'value': 6, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (0, 0), 'value': 3, 'phase': 'update'},
        {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (0, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3, 'parent': (0, 0)},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (1, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5, 'parent': (0, 0)},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (0, 3), 'value': 2, 'phase': 'update'},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (3, 3), 'value': 5, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (0, 1), 'value': 2, 'phase': 'update'},
        {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (1, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5, 'parent': (0, 1)},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (0, 3), 'value': 3, 'phase': 'update'},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (3, 3), 'value': 4, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (1, 1), 'value': 3, 'phase': 'update'},
        {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (3, 3), 'value': 3, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6, 'parent': (1, 1)},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (0, 3), 'value': 4, 'phase': 'update'},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (3, 3), 'value': 5, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (1, 0), 'value': 4, 'phase': 'update'},
        {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'h': 4, 'f': 6, 'parent': (1, 0)},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (0, 3), 'value': 4, 'phase': 'update'},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (3, 3), 'value': 3, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (2, 1), 'value': 3, 'phase': 'update'},
        {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 2), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (0, 3), 'value': 3, 'phase': 'update'},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (3, 3), 'value': 2, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (2, 2), 'value': 2, 'phase': 'update'},
        {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (0, 3), 'value': 2, 'phase': 'update'},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (3, 3), 'value': 1, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (2, 3), 'value': 1, 'phase': 'update'},
        {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (0, 3), 'value': 1, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (1, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7, 'parent': (2, 3)},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6, 'parent': (2, 3)},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (0, 3), 'value': 3, 'phase': 'update'},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (3, 3), 'value': 0, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (3, 3), 'value': 0, 'phase': 'update'},
        {'type': 'pop', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 1},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (0, 3), 'value': 4, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 4, 'phase': 'update'},
        {'type': 'pop_stale', 'state': (3, 2), 'f_stored': 6, 'f_recomputed': 9},
        {'type': 'update_heuristic', 'state': (3, 2), 'h_old': 1, 'h_new': 4},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (0, 3), 'value': 5, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 5, 'phase': 'update'},
        {'type': 'pop_stale', 'state': (3, 1), 'f_stored': 6, 'f_recomputed': 9},
        {'type': 'update_heuristic', 'state': (3, 1), 'h_old': 2, 'h_new': 5},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (0, 3), 'value': 5, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 5, 'phase': 'update'},
        {'type': 'pop_stale', 'state': (2, 0), 'f_stored': 6, 'f_recomputed': 7},
        {'type': 'update_heuristic', 'state': (2, 0), 'h_old': 4, 'h_new': 5},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (0, 3), 'value': 1, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (1, 3), 'value': 1, 'phase': 'update'},
        {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'h_calc', 'state': (0, 3), 'goal': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7, 'parent': (1, 3)},
        {'type': 'h_calc', 'state': (0, 3), 'goal': (0, 3), 'value': 0, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (0, 3), 'value': 0, 'phase': 'update'},
        {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
    ]
    assert actual == expected

def test_agg_recording_lazy1_opt0_vec1() -> None:
    """
    ========================================================================
     Recording test: lazy=True, opt=False, vec=True.
     Pins the full event stream + counter snapshot for kA*_agg
     on grid_4x4_obstacle (Φ=MIN, k=2).
    ========================================================================
    """
    p = _grid_4x4_obstacle_multigoal()
    algo = KAStarAgg(problem=p, h=_manhattan_grid,
                     agg='MIN',
                     is_lazy=True,
                     is_opt=False,
                     store_vector=True,
                     is_recording=True)
    sols = algo.run()
    by_rc = {(g.key.row, g.key.col): s.cost
             for g, s in sols.items()}
    assert by_rc == {(3, 3): 6, (0, 3): 7}
    assert algo.counters == {'cnt_h_search': 25, 'cnt_h_update': 0, 'cnt_phi_search': 13, 'cnt_phi_update': 13, 'cnt_push': 16, 'cnt_pop': 13, 'cnt_pop_stale': 3, 'cnt_decrease': 0}
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'h_calc', 'state': (0, 0), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 0), 'goal': (3, 3), 'value': 6, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (0, 0), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3, 'parent': None},
        {'type': 'phi_calc', 'state': (0, 0), 'value': 3, 'phase': 'update'},
        {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (0, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3, 'parent': (0, 0)},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (1, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5, 'parent': (0, 0)},
        {'type': 'phi_calc', 'state': (0, 1), 'value': 2, 'phase': 'update'},
        {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (1, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5, 'parent': (0, 1)},
        {'type': 'phi_calc', 'state': (1, 1), 'value': 3, 'phase': 'update'},
        {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (3, 3), 'value': 3, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6, 'parent': (1, 1)},
        {'type': 'phi_calc', 'state': (1, 0), 'value': 4, 'phase': 'update'},
        {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'h': 4, 'f': 6, 'parent': (1, 0)},
        {'type': 'phi_calc', 'state': (2, 1), 'value': 3, 'phase': 'update'},
        {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 2), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'phi_calc', 'state': (2, 2), 'value': 2, 'phase': 'update'},
        {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'phi_calc', 'state': (2, 3), 'value': 1, 'phase': 'update'},
        {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (0, 3), 'value': 1, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (1, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7, 'parent': (2, 3)},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6, 'parent': (2, 3)},
        {'type': 'phi_calc', 'state': (3, 3), 'value': 0, 'phase': 'update'},
        {'type': 'pop', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 1},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 4, 'phase': 'update'},
        {'type': 'pop_stale', 'state': (3, 2), 'f_stored': 6, 'f_recomputed': 9},
        {'type': 'update_heuristic', 'state': (3, 2), 'h_old': 1, 'h_new': 4},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 5, 'phase': 'update'},
        {'type': 'pop_stale', 'state': (3, 1), 'f_stored': 6, 'f_recomputed': 9},
        {'type': 'update_heuristic', 'state': (3, 1), 'h_old': 2, 'h_new': 5},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 5, 'phase': 'update'},
        {'type': 'pop_stale', 'state': (2, 0), 'f_stored': 6, 'f_recomputed': 7},
        {'type': 'update_heuristic', 'state': (2, 0), 'h_old': 4, 'h_new': 5},
        {'type': 'phi_calc', 'state': (1, 3), 'value': 1, 'phase': 'update'},
        {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'h_calc', 'state': (0, 3), 'goal': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7, 'parent': (1, 3)},
        {'type': 'phi_calc', 'state': (0, 3), 'value': 0, 'phase': 'update'},
        {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
    ]
    assert actual == expected

def test_agg_recording_lazy1_opt1_vec0() -> None:
    """
    ========================================================================
     Recording test: lazy=True, opt=True, vec=False.
     Pins the full event stream + counter snapshot for kA*_agg
     on grid_4x4_obstacle (Φ=MIN, k=2).
    ========================================================================
    """
    p = _grid_4x4_obstacle_multigoal()
    algo = KAStarAgg(problem=p, h=_manhattan_grid,
                     agg='MIN',
                     is_lazy=True,
                     is_opt=True,
                     store_vector=False,
                     is_recording=True)
    sols = algo.run()
    by_rc = {(g.key.row, g.key.col): s.cost
             for g, s in sols.items()}
    assert by_rc == {(3, 3): 6, (0, 3): 7}
    assert algo.counters == {'cnt_h_search': 25, 'cnt_h_update': 3, 'cnt_phi_search': 13, 'cnt_phi_update': 3, 'cnt_push': 16, 'cnt_pop': 13, 'cnt_pop_stale': 3, 'cnt_decrease': 0}
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'h_calc', 'state': (0, 0), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 0), 'goal': (3, 3), 'value': 6, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (0, 0), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (0, 0), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3, 'parent': None},
        {'type': 'refresh_skip', 'state': (0, 0), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (0, 1), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (0, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3, 'parent': (0, 0)},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (1, 0), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (1, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5, 'parent': (0, 0)},
        {'type': 'refresh_skip', 'state': (0, 1), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (1, 1), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (1, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5, 'parent': (0, 1)},
        {'type': 'refresh_skip', 'state': (1, 1), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (3, 3), 'value': 3, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 1), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6, 'parent': (1, 1)},
        {'type': 'refresh_skip', 'state': (1, 0), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 0), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'h': 4, 'f': 6, 'parent': (1, 0)},
        {'type': 'refresh_skip', 'state': (2, 1), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 2), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 2), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (3, 1), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'refresh_skip', 'state': (2, 2), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 3), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (3, 2), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'refresh_skip', 'state': (2, 3), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (0, 3), 'value': 1, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (1, 3), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (1, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7, 'parent': (2, 3)},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (3, 3), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6, 'parent': (2, 3)},
        {'type': 'refresh_skip', 'state': (3, 3), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 1},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (0, 3), 'value': 4, 'phase': 'update'},
        {'type': 'responsible_set', 'state': (3, 2), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 4, 'phase': 'update'},
        {'type': 'pop_stale', 'state': (3, 2), 'f_stored': 6, 'f_recomputed': 9},
        {'type': 'update_heuristic', 'state': (3, 2), 'h_old': 1, 'h_new': 4},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (0, 3), 'value': 5, 'phase': 'update'},
        {'type': 'responsible_set', 'state': (3, 1), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 5, 'phase': 'update'},
        {'type': 'pop_stale', 'state': (3, 1), 'f_stored': 6, 'f_recomputed': 9},
        {'type': 'update_heuristic', 'state': (3, 1), 'h_old': 2, 'h_new': 5},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (0, 3), 'value': 5, 'phase': 'update'},
        {'type': 'responsible_set', 'state': (2, 0), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 5, 'phase': 'update'},
        {'type': 'pop_stale', 'state': (2, 0), 'f_stored': 6, 'f_recomputed': 7},
        {'type': 'update_heuristic', 'state': (2, 0), 'h_old': 4, 'h_new': 5},
        {'type': 'refresh_skip', 'state': (1, 3), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'h_calc', 'state': (0, 3), 'goal': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (0, 3), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7, 'parent': (1, 3)},
        {'type': 'refresh_skip', 'state': (0, 3), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
    ]
    assert actual == expected

def test_agg_recording_lazy1_opt1_vec1() -> None:
    """
    ========================================================================
     Recording test: lazy=True, opt=True, vec=True.
     Pins the full event stream + counter snapshot for kA*_agg
     on grid_4x4_obstacle (Φ=MIN, k=2).
    ========================================================================
    """
    p = _grid_4x4_obstacle_multigoal()
    algo = KAStarAgg(problem=p, h=_manhattan_grid,
                     agg='MIN',
                     is_lazy=True,
                     is_opt=True,
                     store_vector=True,
                     is_recording=True)
    sols = algo.run()
    by_rc = {(g.key.row, g.key.col): s.cost
             for g, s in sols.items()}
    assert by_rc == {(3, 3): 6, (0, 3): 7}
    assert algo.counters == {'cnt_h_search': 25, 'cnt_h_update': 0, 'cnt_phi_search': 13, 'cnt_phi_update': 3, 'cnt_push': 16, 'cnt_pop': 13, 'cnt_pop_stale': 3, 'cnt_decrease': 0}
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'h_calc', 'state': (0, 0), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 0), 'goal': (3, 3), 'value': 6, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (0, 0), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (0, 0), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3, 'parent': None},
        {'type': 'refresh_skip', 'state': (0, 0), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (0, 1), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (0, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3, 'parent': (0, 0)},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (1, 0), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (1, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5, 'parent': (0, 0)},
        {'type': 'refresh_skip', 'state': (0, 1), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (1, 1), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (1, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5, 'parent': (0, 1)},
        {'type': 'refresh_skip', 'state': (1, 1), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (3, 3), 'value': 3, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 1), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6, 'parent': (1, 1)},
        {'type': 'refresh_skip', 'state': (1, 0), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 0), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'h': 4, 'f': 6, 'parent': (1, 0)},
        {'type': 'refresh_skip', 'state': (2, 1), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 2), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 2), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (3, 1), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'refresh_skip', 'state': (2, 2), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 3), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (3, 2), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'refresh_skip', 'state': (2, 3), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (0, 3), 'value': 1, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (1, 3), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (1, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7, 'parent': (2, 3)},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (3, 3), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6, 'parent': (2, 3)},
        {'type': 'refresh_skip', 'state': (3, 3), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 1},
        {'type': 'responsible_set', 'state': (3, 2), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 4, 'phase': 'update'},
        {'type': 'pop_stale', 'state': (3, 2), 'f_stored': 6, 'f_recomputed': 9},
        {'type': 'update_heuristic', 'state': (3, 2), 'h_old': 1, 'h_new': 4},
        {'type': 'responsible_set', 'state': (3, 1), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 5, 'phase': 'update'},
        {'type': 'pop_stale', 'state': (3, 1), 'f_stored': 6, 'f_recomputed': 9},
        {'type': 'update_heuristic', 'state': (3, 1), 'h_old': 2, 'h_new': 5},
        {'type': 'responsible_set', 'state': (2, 0), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 5, 'phase': 'update'},
        {'type': 'pop_stale', 'state': (2, 0), 'f_stored': 6, 'f_recomputed': 7},
        {'type': 'update_heuristic', 'state': (2, 0), 'h_old': 4, 'h_new': 5},
        {'type': 'refresh_skip', 'state': (1, 3), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'h_calc', 'state': (0, 3), 'goal': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (0, 3), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7, 'parent': (1, 3)},
        {'type': 'refresh_skip', 'state': (0, 3), 'reason': 'lazy_responsible_active'},
        {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
    ]
    assert actual == expected

def test_agg_recording_lazy0_opt0_vec0() -> None:
    """
    ========================================================================
     Recording test: lazy=False, opt=False, vec=False.
     Pins the full event stream + counter snapshot for kA*_agg
     on grid_4x4_obstacle (Φ=MIN, k=2).
    ========================================================================
    """
    p = _grid_4x4_obstacle_multigoal()
    algo = KAStarAgg(problem=p, h=_manhattan_grid,
                     agg='MIN',
                     is_lazy=False,
                     is_opt=False,
                     store_vector=False,
                     is_recording=True)
    sols = algo.run()
    by_rc = {(g.key.row, g.key.col): s.cost
             for g, s in sols.items()}
    assert by_rc == {(3, 3): 6, (0, 3): 7}
    assert algo.counters == {'cnt_h_search': 25, 'cnt_h_update': 4, 'cnt_phi_search': 13, 'cnt_phi_update': 4, 'cnt_push': 17, 'cnt_pop': 10, 'cnt_pop_stale': 0, 'cnt_decrease': 0}
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'h_calc', 'state': (0, 0), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 0), 'goal': (3, 3), 'value': 6, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (0, 0), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3, 'parent': None},
        {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (0, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3, 'parent': (0, 0)},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (1, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5, 'parent': (0, 0)},
        {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (1, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5, 'parent': (0, 1)},
        {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (3, 3), 'value': 3, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6, 'parent': (1, 1)},
        {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'h': 4, 'f': 6, 'parent': (1, 0)},
        {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 2), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (0, 3), 'value': 1, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (1, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7, 'parent': (2, 3)},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6, 'parent': (2, 3)},
        {'type': 'pop', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 1},
        {'type': 'update_frontier', 'num_nodes': 4, 'next_goal_index': 0},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (0, 3), 'value': 4, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 4, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (3, 2), 'h_old': 1, 'h_new': 4},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (0, 3), 'value': 5, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 5, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (3, 1), 'h_old': 2, 'h_new': 5},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (0, 3), 'value': 5, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 5, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (2, 0), 'h_old': 4, 'h_new': 5},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (0, 3), 'value': 1, 'phase': 'update'},
        {'type': 'phi_calc', 'state': (1, 3), 'value': 1, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (1, 3), 'h_old': 1, 'h_new': 1},
        {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'h_calc', 'state': (0, 3), 'goal': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7, 'parent': (1, 3)},
        {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
    ]
    assert actual == expected

def test_agg_recording_lazy0_opt0_vec1() -> None:
    """
    ========================================================================
     Recording test: lazy=False, opt=False, vec=True.
     Pins the full event stream + counter snapshot for kA*_agg
     on grid_4x4_obstacle (Φ=MIN, k=2).
    ========================================================================
    """
    p = _grid_4x4_obstacle_multigoal()
    algo = KAStarAgg(problem=p, h=_manhattan_grid,
                     agg='MIN',
                     is_lazy=False,
                     is_opt=False,
                     store_vector=True,
                     is_recording=True)
    sols = algo.run()
    by_rc = {(g.key.row, g.key.col): s.cost
             for g, s in sols.items()}
    assert by_rc == {(3, 3): 6, (0, 3): 7}
    assert algo.counters == {'cnt_h_search': 25, 'cnt_h_update': 0, 'cnt_phi_search': 13, 'cnt_phi_update': 4, 'cnt_push': 17, 'cnt_pop': 10, 'cnt_pop_stale': 0, 'cnt_decrease': 0}
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'h_calc', 'state': (0, 0), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 0), 'goal': (3, 3), 'value': 6, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (0, 0), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3, 'parent': None},
        {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (0, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3, 'parent': (0, 0)},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (1, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5, 'parent': (0, 0)},
        {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (1, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5, 'parent': (0, 1)},
        {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (3, 3), 'value': 3, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6, 'parent': (1, 1)},
        {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'h': 4, 'f': 6, 'parent': (1, 0)},
        {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 2), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (2, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (0, 3), 'value': 1, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (1, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7, 'parent': (2, 3)},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6, 'parent': (2, 3)},
        {'type': 'pop', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 1},
        {'type': 'update_frontier', 'num_nodes': 4, 'next_goal_index': 0},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 4, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (3, 2), 'h_old': 1, 'h_new': 4},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 5, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (3, 1), 'h_old': 2, 'h_new': 5},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 5, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (2, 0), 'h_old': 4, 'h_new': 5},
        {'type': 'phi_calc', 'state': (1, 3), 'value': 1, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (1, 3), 'h_old': 1, 'h_new': 1},
        {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'h_calc', 'state': (0, 3), 'goal': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'phi_calc', 'state': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7, 'parent': (1, 3)},
        {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
    ]
    assert actual == expected

def test_agg_recording_lazy0_opt1_vec0() -> None:
    """
    ========================================================================
     Recording test: lazy=False, opt=True, vec=False.
     Pins the full event stream + counter snapshot for kA*_agg
     on grid_4x4_obstacle (Φ=MIN, k=2).
    ========================================================================
    """
    p = _grid_4x4_obstacle_multigoal()
    algo = KAStarAgg(problem=p, h=_manhattan_grid,
                     agg='MIN',
                     is_lazy=False,
                     is_opt=True,
                     store_vector=False,
                     is_recording=True)
    sols = algo.run()
    by_rc = {(g.key.row, g.key.col): s.cost
             for g, s in sols.items()}
    assert by_rc == {(3, 3): 6, (0, 3): 7}
    assert algo.counters == {'cnt_h_search': 25, 'cnt_h_update': 3, 'cnt_phi_search': 13, 'cnt_phi_update': 3, 'cnt_push': 17, 'cnt_pop': 10, 'cnt_pop_stale': 0, 'cnt_decrease': 0}
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'h_calc', 'state': (0, 0), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 0), 'goal': (3, 3), 'value': 6, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (0, 0), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (0, 0), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3, 'parent': None},
        {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (0, 1), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (0, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3, 'parent': (0, 0)},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (1, 0), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (1, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5, 'parent': (0, 0)},
        {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (1, 1), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (1, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5, 'parent': (0, 1)},
        {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (3, 3), 'value': 3, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 1), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6, 'parent': (1, 1)},
        {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 0), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'h': 4, 'f': 6, 'parent': (1, 0)},
        {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 2), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 2), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (3, 1), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 3), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (3, 2), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (0, 3), 'value': 1, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (1, 3), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (1, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7, 'parent': (2, 3)},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (3, 3), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6, 'parent': (2, 3)},
        {'type': 'pop', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 1},
        {'type': 'update_frontier', 'num_nodes': 4, 'next_goal_index': 0},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (0, 3), 'value': 4, 'phase': 'update'},
        {'type': 'responsible_set', 'state': (3, 2), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 4, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (3, 2), 'h_old': 1, 'h_new': 4},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (0, 3), 'value': 5, 'phase': 'update'},
        {'type': 'responsible_set', 'state': (3, 1), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 5, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (3, 1), 'h_old': 2, 'h_new': 5},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (0, 3), 'value': 5, 'phase': 'update'},
        {'type': 'responsible_set', 'state': (2, 0), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 5, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (2, 0), 'h_old': 4, 'h_new': 5},
        {'type': 'refresh_skip', 'state': (1, 3), 'reason': 'eager_responsible_unchanged'},
        {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'h_calc', 'state': (0, 3), 'goal': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (0, 3), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7, 'parent': (1, 3)},
        {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
    ]
    assert actual == expected

def test_agg_recording_lazy0_opt1_vec1() -> None:
    """
    ========================================================================
     Recording test: lazy=False, opt=True, vec=True.
     Pins the full event stream + counter snapshot for kA*_agg
     on grid_4x4_obstacle (Φ=MIN, k=2).
    ========================================================================
    """
    p = _grid_4x4_obstacle_multigoal()
    algo = KAStarAgg(problem=p, h=_manhattan_grid,
                     agg='MIN',
                     is_lazy=False,
                     is_opt=True,
                     store_vector=True,
                     is_recording=True)
    sols = algo.run()
    by_rc = {(g.key.row, g.key.col): s.cost
             for g, s in sols.items()}
    assert by_rc == {(3, 3): 6, (0, 3): 7}
    assert algo.counters == {'cnt_h_search': 25, 'cnt_h_update': 0, 'cnt_phi_search': 13, 'cnt_phi_update': 3, 'cnt_push': 17, 'cnt_pop': 10, 'cnt_pop_stale': 0, 'cnt_decrease': 0}
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'h_calc', 'state': (0, 0), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 0), 'goal': (3, 3), 'value': 6, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (0, 0), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (0, 0), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3, 'parent': None},
        {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (0, 1), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (0, 1), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (0, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3, 'parent': (0, 0)},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 0), 'goal': (3, 3), 'value': 5, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (1, 0), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (1, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5, 'parent': (0, 0)},
        {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 1), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (1, 1), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (1, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5, 'parent': (0, 1)},
        {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 1), 'goal': (3, 3), 'value': 3, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 1), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 1), 'value': 3, 'phase': 'search'},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6, 'parent': (1, 1)},
        {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 0), 'goal': (3, 3), 'value': 4, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 0), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 4, 'phase': 'search'},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'h': 4, 'f': 6, 'parent': (1, 0)},
        {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 2), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 2), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 2), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (0, 3), 'value': 5, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 1), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (3, 1), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 2, 'phase': 'search'},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
        {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (0, 3), 'value': 2, 'phase': 'search'},
        {'type': 'h_calc', 'state': (2, 3), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (2, 3), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (2, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (0, 3), 'value': 4, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 2), 'goal': (3, 3), 'value': 1, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (3, 2), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
        {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (0, 3), 'value': 1, 'phase': 'search'},
        {'type': 'h_calc', 'state': (1, 3), 'goal': (3, 3), 'value': 2, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (1, 3), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (1, 3), 'value': 1, 'phase': 'search'},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7, 'parent': (2, 3)},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (0, 3), 'value': 3, 'phase': 'search'},
        {'type': 'h_calc', 'state': (3, 3), 'goal': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (3, 3), 'responsible': (3, 3)},
        {'type': 'phi_calc', 'state': (3, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6, 'parent': (2, 3)},
        {'type': 'pop', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
        {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 1},
        {'type': 'update_frontier', 'num_nodes': 4, 'next_goal_index': 0},
        {'type': 'responsible_set', 'state': (3, 2), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (3, 2), 'value': 4, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (3, 2), 'h_old': 1, 'h_new': 4},
        {'type': 'responsible_set', 'state': (3, 1), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (3, 1), 'value': 5, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (3, 1), 'h_old': 2, 'h_new': 5},
        {'type': 'responsible_set', 'state': (2, 0), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (2, 0), 'value': 5, 'phase': 'update'},
        {'type': 'update_heuristic', 'state': (2, 0), 'h_old': 4, 'h_new': 5},
        {'type': 'refresh_skip', 'state': (1, 3), 'reason': 'eager_responsible_unchanged'},
        {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'h_calc', 'state': (0, 3), 'goal': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'responsible_set', 'state': (0, 3), 'responsible': (0, 3)},
        {'type': 'phi_calc', 'state': (0, 3), 'value': 0, 'phase': 'search'},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7, 'parent': (1, 3)},
        {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
        {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
    ]
    assert actual == expected
