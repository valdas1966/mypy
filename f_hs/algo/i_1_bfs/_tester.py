import pytest
from f_hs.algo.i_1_bfs import BFS
from f_hs.problem import ProblemSPP


@pytest.fixture
def abc() -> BFS:
    """
    ========================================================================
     BFS on linear Graph: A -> B -> C.
    ========================================================================
    """
    return BFS.Factory.graph_abc()


@pytest.fixture
def no_path() -> BFS:
    """
    ========================================================================
     BFS on Graph with no path to goal.
    ========================================================================
    """
    return BFS.Factory.graph_no_path()


@pytest.fixture
def start_is_goal() -> BFS:
    """
    ========================================================================
     BFS where start equals goal.
    ========================================================================
    """
    return BFS.Factory.graph_start_is_goal()


@pytest.fixture
def diamond() -> BFS:
    """
    ========================================================================
     BFS on diamond Graph.
    ========================================================================
    """
    return BFS.Factory.graph_diamond()


def test_path_found(abc: BFS) -> None:
    """
    ========================================================================
     Test that BFS finds the optimal path.
    ========================================================================
    """
    solution = abc.run()
    assert bool(solution) is True
    assert solution.cost == 2.0
    path = abc.reconstruct_path()
    assert len(path) == 3
    assert path[0].key == 'A'
    assert path[-1].key == 'C'


def test_no_path(no_path: BFS) -> None:
    """
    ========================================================================
     Test that BFS returns invalid when no path exists.
    ========================================================================
    """
    solution = no_path.run()
    assert bool(solution) is False
    assert solution.cost == float('inf')


def test_start_is_goal(start_is_goal: BFS) -> None:
    """
    ========================================================================
     Test that BFS handles start == goal.
    ========================================================================
    """
    solution = start_is_goal.run()
    assert bool(solution) is True
    assert solution.cost == 0.0
    path = start_is_goal.reconstruct_path()
    assert len(path) == 1
    assert path[0].key == 'A'


def test_diamond(diamond: BFS) -> None:
    """
    ========================================================================
     Test that BFS finds optimal path on diamond graph.
    ========================================================================
    """
    solution = diamond.run()
    assert bool(solution) is True
    assert solution.cost == 2.0
    path = diamond.reconstruct_path()
    assert len(path) == 3
    assert path[0].key == 'A'
    assert path[-1].key == 'D'


def test_recording() -> None:
    """
    ========================================================================
     Test that events are recorded when is_recording=True.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    algo = BFS(problem=problem, is_recording=True)
    solution = algo.run()
    path = algo.reconstruct_path()
    events = algo.recorder.events
    types = [e['type'] for e in events]
    assert 'push' in types
    assert 'pop' in types
    for e in events:
        assert 'duration' in e
        assert e['duration'] >= 0


def test_no_recording() -> None:
    """
    ========================================================================
     Test that no events are recorded when is_recording=False.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    algo = BFS(problem=problem, is_recording=False)
    algo.run()
    assert len(algo.recorder) == 0


def test_elapsed(abc: BFS) -> None:
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
def grid_3x3() -> BFS:
    """
    ========================================================================
     BFS on open 3x3 Grid.
    ========================================================================
    """
    return BFS.Factory.grid_3x3()


def test_grid_path_found(grid_3x3: BFS) -> None:
    """
    ========================================================================
     Test BFS on 3x3 grid finds optimal path (cost 4).
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
     Test BFS on 3x3 grid with obstacle still finds path.
    ========================================================================
    """
    algo = BFS.Factory.grid_3x3_obstacle()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 4.0


def test_grid_no_path() -> None:
    """
    ========================================================================
     Test BFS on 3x3 grid with wall returns invalid.
    ========================================================================
    """
    algo = BFS.Factory.grid_3x3_no_path()
    solution = algo.run()
    assert bool(solution) is False
    assert solution.cost == float('inf')


def test_grid_start_is_goal() -> None:
    """
    ========================================================================
     Test BFS on grid where start equals goal.
    ========================================================================
    """
    algo = BFS.Factory.grid_3x3_start_is_goal()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 0.0
    path = algo.reconstruct_path()
    assert len(path) == 1
