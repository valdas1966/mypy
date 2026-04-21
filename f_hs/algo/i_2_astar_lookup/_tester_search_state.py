from f_ds.grids.cell.i_1_map import CellMap
from f_ds.grids.grid.map import GridMap

from f_hs.algo.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_1_astar import AStar
from f_hs.algo.i_2_astar_lookup import AStarLookup
from f_hs.algo.i_2_astar_lookup._utils import normalize
from f_hs.frontier.i_1_priority.main import FrontierPriority
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase
from f_hs.state.i_1_cell.main import StateCell


def test_resume_auto_refreshes_stale_frontier_priorities() -> None:
    """
    ========================================================================
     Inject a SearchStateSPP whose frontier entry was pushed
     with a DELIBERATELY WRONG priority. resume() auto-refreshes
     on first call (dirty flag set at __init__ because
     search_state was supplied), then pumps to optimal.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    a = StateBase[str](key='A')
    b = StateBase[str](key='B')

    seed = SearchStateSPP[StateBase[str]](
        frontier=FrontierPriority[StateBase[str]](),
        g={a: 0.0, b: 1.0},
        parent={a: None, b: a},
        closed={a},
    )
    seed.frontier.push(state=b, priority=(999.0, 0, 1, b))

    h_map = {'A': 2, 'B': 1, 'C': 0}
    algo = AStar(
        problem=problem,
        h=lambda s: h_map.get(s.key, 0),
        search_state=seed,
    )
    
    assert algo._frontier_dirty is True

    sol = algo.resume()
    assert sol.cost == 2
    assert algo._frontier_dirty is False
    assert algo.search_state.goal_reached is not None
    assert algo.search_state.goal_reached.key == 'C'

    algo.resume()
    assert algo._frontier_dirty is False


def test_recording_resume_from_seeded_search_state() -> None:
    """
    ========================================================================
     Inject a pre-built SearchStateSPP into AStarLookup and pump
     with resume(). Records only the post-seed events:
     pop(B), push(C), pop(C).
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    a = StateBase[str](key='A')
    b = StateBase[str](key='B')

    seed = SearchStateSPP[StateBase[str]](
        frontier=FrontierPriority[StateBase[str]](),
        g={a: 0.0, b: 1.0},
        parent={a: None, b: a},
        closed={a},
    )
    h_map = {'A': 2, 'B': 1, 'C': 0}
    algo = AStar(
        problem=problem,
        h=lambda s: h_map.get(s.key, 0),
        is_recording=True,
        search_state=seed,
    )
    
    seed.frontier.push(state=b, priority=algo._priority(state=b))

    sol = algo.resume()
    assert sol.cost == 2

    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 1, 'f': 2},
        {'type': 'push', 'state': 'C', 'g': 2, 'parent': 'B', 'h': 0, 'f': 2},
        {'type': 'pop',  'state': 'C', 'g': 2, 'h': 0, 'f': 2},
    ]
    assert actual == expected
    for e in actual:
        assert e['state'] != 'A'
        if 'parent' in e:
            assert e['parent'] != 'A'
    assert algo.search_state is seed
    assert seed.goal_reached is not None
    assert seed.goal_reached.key == 'C'


def test_recording_grid_4x4_reuse_state_from_prior_goal_2_1(
        ) -> None:
    """
    ========================================================================
     Two-stage AStar on grid_4x4_obstacle:
     Stage 1 (simple): (0,0) -> (2,1). Keep final state.
     Stage 2 (Pro, recorded): inject state, change goal to
     (0,3), resume. Pins dirty-flag lifecycle, goal_reached
     overwrite, parent rewrites, auto-refresh.
    ========================================================================
    """
    grid = GridMap(rows=4)
    grid[0][2].set_invalid()
    grid[1][2].set_invalid()
    problem_first = ProblemGrid(
        grid=grid,
        start=grid[0][0],
        goal=grid[2][1],
    )
    goal_first = problem_first.goal
    algo_first = AStar(
        problem=problem_first,
        h=lambda s: s.distance(goal_first),
    )
    sol_first = algo_first.run()
    assert sol_first.cost == 3
    assert algo_first.search_state.goal_reached.rc == (2, 1)

    problem_second = ProblemGrid.Factory.grid_4x4_obstacle()
    goal_second = problem_second.goal
    algo_second = AStar(
        problem=problem_second,
        h=lambda s: s.distance(goal_second),
        is_recording=True,
        search_state=algo_first.search_state,
    )
    
    assert algo_second._frontier_dirty is True
    assert algo_second.search_state.goal_reached.rc == (2, 1)

    sol = algo_second.resume()
    assert sol.cost == 7
    assert algo_second._frontier_dirty is False
    assert algo_second.search_state.goal_reached is not None
    assert algo_second.search_state.goal_reached.rc == (0, 3)

    actual = [normalize(e) for e in algo_second.recorder.events]
    expected = [
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (2, 0), 'g': 2, 'h': 5, 'f': 7},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (2, 0), 'h': 4, 'f': 7},
        {'type': 'push', 'state': (3, 0), 'g': 3, 'parent': (2, 0), 'h': 6, 'f': 9},
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
    assert len(actual) == 17

    for e in actual:
        assert 'is_cached' not in e

    parent_21 = algo_second.search_state.parent[
        StateCell(key=CellMap(row=2, col=1))]
    assert parent_21.rc == (2, 0)
    assert algo_second.search_state.g[
        StateCell(key=CellMap(row=2, col=1))] == 3.0
