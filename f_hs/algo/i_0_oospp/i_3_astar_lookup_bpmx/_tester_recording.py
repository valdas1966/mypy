"""
============================================================================
 AStarLookupBPMX — full event-stream pin on the canonical
 OOSPP problem (`grid_4x4_obstacle`: start (0,0), goal (0,3),
 cost 7; no cache; full BPMX cascade).
============================================================================
"""

from f_hs.algo.i_0_oospp.i_3_astar_lookup_bpmx import AStarLookupBPMX
from f_hs.algo.u_event_normalize import normalize
from f_hs.problem.i_1_grid import ProblemGrid


def test_recording_canonical_oospp() -> None:
    """
    ========================================================================
     Pin the FULL event stream for AStarLookupBPMX (no cache,
     full BPMX cascade) on the canonical OOSPP problem (30
     events: AStar trace + 8 `bpmx_iteration` markers, all
     settling at iteration 1 with no lifts under consistent
     Manhattan h).
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = p.goal
    algo = AStarLookupBPMX(
        problem=p,
        h=lambda s: float(s.distance(goal)),
        rule_bpmx='CASCADE',
        depth_bpmx=None,
        is_recording=True,
    )
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'bpmx_iteration', 'state': (0, 0), 'iteration': 1, 'num_levels': 8, 'num_states': 14},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'bpmx_iteration', 'state': (0, 1), 'iteration': 1, 'num_levels': 7, 'num_states': 14},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 3, 'f': 5},
        {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'bpmx_iteration', 'state': (1, 1), 'iteration': 1, 'num_levels': 6, 'num_states': 14},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'bpmx_iteration', 'state': (1, 0), 'iteration': 1, 'num_levels': 7, 'num_states': 14},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (2, 1), 'iteration': 1, 'num_levels': 5, 'num_states': 14},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (2, 2), 'iteration': 1, 'num_levels': 5, 'num_states': 14},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (2, 3), 'iteration': 1, 'num_levels': 6, 'num_states': 14},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'bpmx_iteration', 'state': (1, 3), 'iteration': 1, 'num_levels': 7, 'num_states': 14},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected
