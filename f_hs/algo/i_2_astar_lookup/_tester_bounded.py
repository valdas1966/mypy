from f_ds.grids.cell.i_1_map import CellMap

from f_hs.algo.i_1_astar import AStar
from f_hs.algo.i_2_astar_lookup import AStarLookup
from f_hs.algo.i_2_astar_lookup._utils import normalize
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_1_cell.main import StateCell


def test_astar_with_hbounded_finds_optimal_cost() -> None:
    """
    ========================================================================
     AStar on grid_4x4_obstacle with Manhattan wrapped in
     HBounded — bound (1,0) at h=6 and (2,0) at h=5 (both
     tight). Admissibility preserved (optimal cost 7); bounded
     pop count ≤ un-bounded baseline.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem_b = ProblemGrid.Factory.grid_4x4_obstacle()
    goal_b = problem_b.goal
    base_algo = AStar(
        problem=problem_b,
        h=lambda s: s.distance(goal_b),
        is_recording=True,
    )
    base_algo.run()
    base_pops = sum(1 for e in base_algo.recorder.events
                    if e.get('type') == 'pop')

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {sc(1, 0): 6, sc(2, 0): 5}
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds=bounds,
    )
    algo = AStarLookup(problem=problem, h=h, is_recording=True)
    
    sol = algo.run()
    assert sol.cost == 7

    bounded_pops = sum(1 for e in algo.recorder.events
                       if e.get('type') == 'pop')
    assert bounded_pops <= base_pops


def test_recording_hbounded_tightens_h_on_grid_4x4_obstacle(
        ) -> None:
    """
    ========================================================================
     HBounded bounds (1,0) at h=6 (tight; h*((1,0))=6). (1,0)'s
     bump to f=7 dominates it out of the pop set. Pins
     is_bounded on push-only of a pruned state.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {sc(1, 0): 6}
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds=bounds,
    )
    algo = AStarLookup(problem=problem, h=h, is_recording=True)
    
    sol = algo.run()
    assert sol.cost == 7

    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 3, 'f': 5},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'push', 'state': (2, 0), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected
    assert len(actual) == 21

    popped_states = {e['state'] for e in actual
                     if e['type'] == 'pop'}
    assert (1, 0) not in popped_states
    push_10 = [e for e in actual
               if e['type'] == 'push' and e['state'] == (1, 0)][0]
    assert push_10['h'] == 6 and push_10['f'] == 7
    assert push_10.get('is_bounded') is True
    for e in actual:
        if e['state'] != (1, 0):
            assert 'is_bounded' not in e
    for e in actual:
        assert 'is_cached' not in e


def test_recording_hbounded_popped_state_on_grid_4x4_obstacle(
        ) -> None:
    """
    ========================================================================
     HBounded bounds (1,1) at h=5 (tight). (1,1) IS popped, so
     is_bounded=True appears on BOTH push AND pop.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {sc(1, 1): 5}
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds=bounds,
    )
    algo = AStarLookup(problem=problem, h=h, is_recording=True)
    sol = algo.run()
    assert sol.cost == 7

    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected
    assert len(actual) == 22

    bounded = [e for e in actual if e.get('is_bounded')]
    assert len(bounded) == 2
    assert {e['type'] for e in bounded} == {'push', 'pop'}
    assert all(e['state'] == (1, 1) for e in bounded)
    for e in actual:
        if e['state'] != (1, 1):
            assert 'is_bounded' not in e
    for e in actual:
        assert 'is_cached' not in e
