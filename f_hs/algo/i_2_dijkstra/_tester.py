import pytest
from f_hs.algo.i_2_dijkstra import Dijkstra


@pytest.fixture
def abc() -> Dijkstra:
    """
    ========================================================================
     Dijkstra on linear Graph: A -> B -> C.
    ========================================================================
    """
    return Dijkstra.Factory.graph_abc()


@pytest.fixture
def no_path() -> Dijkstra:
    """
    ========================================================================
     Dijkstra on Graph with no path to goal.
    ========================================================================
    """
    return Dijkstra.Factory.graph_no_path()


@pytest.fixture
def start_is_goal() -> Dijkstra:
    """
    ========================================================================
     Dijkstra where start equals goal.
    ========================================================================
    """
    return Dijkstra.Factory.graph_start_is_goal()


@pytest.fixture
def diamond() -> Dijkstra:
    """
    ========================================================================
     Dijkstra on diamond Graph.
    ========================================================================
    """
    return Dijkstra.Factory.graph_diamond()


def test_path_found(abc: Dijkstra) -> None:
    """
    ========================================================================
     Test that Dijkstra finds the optimal path.
    ========================================================================
    """
    solution = abc.run()
    assert bool(solution) is True
    assert solution.cost == 2.0
    path = abc.reconstruct_path()
    assert len(path) == 3
    assert path[0].key == 'A'
    assert path[-1].key == 'C'


def test_no_path(no_path: Dijkstra) -> None:
    """
    ========================================================================
     Test that Dijkstra returns invalid when no path exists.
    ========================================================================
    """
    solution = no_path.run()
    assert bool(solution) is False
    assert solution.cost == float('inf')


def test_start_is_goal(start_is_goal: Dijkstra) -> None:
    """
    ========================================================================
     Test that Dijkstra handles start == goal.
    ========================================================================
    """
    solution = start_is_goal.run()
    assert bool(solution) is True
    assert solution.cost == 0.0
    path = start_is_goal.reconstruct_path()
    assert len(path) == 1
    assert path[0].key == 'A'


def test_diamond(diamond: Dijkstra) -> None:
    """
    ========================================================================
     Test that Dijkstra finds optimal path on diamond graph.
    ========================================================================
    """
    solution = diamond.run()
    assert bool(solution) is True
    assert solution.cost == 2.0
    path = diamond.reconstruct_path()
    assert len(path) == 3
    assert path[0].key == 'A'
    assert path[-1].key == 'D'


# ── Grid Tests ───────────────────────────────────────────


@pytest.fixture
def grid_3x3() -> Dijkstra:
    """
    ========================================================================
     Dijkstra on open 3x3 Grid.
    ========================================================================
    """
    return Dijkstra.Factory.grid_3x3()


def test_grid_path_found(grid_3x3: Dijkstra) -> None:
    """
    ========================================================================
     Test Dijkstra on 3x3 grid finds optimal path (cost 4).
    ========================================================================
    """
    solution = grid_3x3.run()
    assert bool(solution) is True
    assert solution.cost == 4.0
    path = grid_3x3.reconstruct_path()
    assert len(path) == 5


def test_grid_obstacle() -> None:
    """
    ========================================================================
     Test Dijkstra on 3x3 grid with obstacle still finds path.
    ========================================================================
    """
    algo = Dijkstra.Factory.grid_3x3_obstacle()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 4.0


def test_grid_no_path() -> None:
    """
    ========================================================================
     Test Dijkstra on 3x3 grid with wall returns invalid.
    ========================================================================
    """
    algo = Dijkstra.Factory.grid_3x3_no_path()
    solution = algo.run()
    assert bool(solution) is False


def test_grid_start_is_goal() -> None:
    """
    ========================================================================
     Test Dijkstra on grid where start equals goal.
    ========================================================================
    """
    algo = Dijkstra.Factory.grid_3x3_start_is_goal()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 0.0
