import pytest
from f_hs.algo.i_1_astar import AStar
from f_hs.problem import ProblemSPP


@pytest.fixture
def abc() -> AStar:
    """
    ========================================================================
     A* on linear Graph: A -> B -> C.
    ========================================================================
    """
    return AStar.Factory.graph_abc()


@pytest.fixture
def no_path() -> AStar:
    """
    ========================================================================
     A* on Graph with no path to goal.
    ========================================================================
    """
    return AStar.Factory.graph_no_path()


@pytest.fixture
def start_is_goal() -> AStar:
    """
    ========================================================================
     A* where start equals goal.
    ========================================================================
    """
    return AStar.Factory.graph_start_is_goal()


@pytest.fixture
def diamond() -> AStar:
    """
    ========================================================================
     A* on diamond Graph.
    ========================================================================
    """
    return AStar.Factory.graph_diamond()


def test_path_found(abc: AStar) -> None:
    """
    ========================================================================
     Test that A* finds the optimal path.
    ========================================================================
    """
    solution = abc.run()
    assert bool(solution) is True
    assert solution.cost == 2.0
    path = abc.reconstruct_path()
    assert len(path) == 3
    assert path[0].key == 'A'
    assert path[-1].key == 'C'


def test_no_path(no_path: AStar) -> None:
    """
    ========================================================================
     Test that A* returns invalid when no path exists.
    ========================================================================
    """
    solution = no_path.run()
    assert bool(solution) is False
    assert solution.cost == float('inf')


def test_start_is_goal(start_is_goal: AStar) -> None:
    """
    ========================================================================
     Test that A* handles start == goal.
    ========================================================================
    """
    solution = start_is_goal.run()
    assert bool(solution) is True
    assert solution.cost == 0.0
    path = start_is_goal.reconstruct_path()
    assert len(path) == 1
    assert path[0].key == 'A'


def test_diamond(diamond: AStar) -> None:
    """
    ========================================================================
     Test that A* finds optimal path on diamond graph.
    ========================================================================
    """
    solution = diamond.run()
    assert bool(solution) is True
    assert solution.cost == 2.0
    path = diamond.reconstruct_path()
    assert len(path) == 3
    assert path[0].key == 'A'
    assert path[-1].key == 'D'


def test_recording_h_values() -> None:
    """
    ========================================================================
     Test that A* events include h and f values.
    ========================================================================
    """
    h_map = {'A': 2.0, 'B': 1.0, 'C': 0.0}
    algo = AStar(
        problem=ProblemSPP.Factory.graph_abc(),
        h=lambda s: h_map.get(s.key, 0.0),
        is_recording=True
    )
    algo.run()
    events = algo.recorder.events
    pushes = [e for e in events if e['type'] == 'push']
    pops = [e for e in events if e['type'] == 'pop']
    for e in pushes:
        assert 'h' in e
        assert 'f' in e
        assert e['f'] == e['g'] + e['h']
    for e in pops:
        assert 'h' in e
        assert 'f' in e
    # Last pop is the goal — h should be 0
    assert pops[-1]['h'] == 0.0


def test_elapsed(abc: AStar) -> None:
    """
    ========================================================================
     Test that elapsed time is set after run.
    ========================================================================
    """
    abc.run()
    assert abc.elapsed is not None
    assert abc.elapsed >= 0


# ── Grid Tests ───────────────────────────────────────────


@pytest.fixture
def grid_3x3() -> AStar:
    """
    ========================================================================
     A* on open 3x3 Grid with Manhattan heuristic.
    ========================================================================
    """
    return AStar.Factory.grid_3x3()


def test_grid_path_found(grid_3x3: AStar) -> None:
    """
    ========================================================================
     Test A* on 3x3 grid finds optimal path (cost 4).
    ========================================================================
    """
    solution = grid_3x3.run()
    assert bool(solution) is True
    assert solution.cost == 4.0
    path = grid_3x3.reconstruct_path()
    assert len(path) == 5
    assert path[0].key.row == 0 and path[0].key.col == 0
    assert path[-1].key.row == 2 and path[-1].key.col == 2


def test_grid_obstacle() -> None:
    """
    ========================================================================
     Test A* on 3x3 grid with obstacle still finds path.
    ========================================================================
    """
    algo = AStar.Factory.grid_3x3_obstacle()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 4.0


def test_grid_no_path() -> None:
    """
    ========================================================================
     Test A* on 3x3 grid with wall returns invalid.
    ========================================================================
    """
    algo = AStar.Factory.grid_3x3_no_path()
    solution = algo.run()
    assert bool(solution) is False
    assert solution.cost == float('inf')


def test_grid_start_is_goal() -> None:
    """
    ========================================================================
     Test A* on grid where start equals goal.
    ========================================================================
    """
    algo = AStar.Factory.grid_3x3_start_is_goal()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 0.0
