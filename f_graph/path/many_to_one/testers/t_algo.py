from f_graph.path.many_to_one.generators.g_algo import GenAlgoManyToOne
from f_graph.path.generators.g_graph import GenGraphPath, NodePath as Node
import pytest


@pytest.fixture
def paths_true() -> dict[Node, list[Node]]:
    """
    ========================================================================
     Fixture for the paths of the 3x3-Grid-Problem.
    ========================================================================
    """
    graph = GenGraphPath.gen_3x3()
    start_1 = graph[0, 2]
    start_2 = graph[2, 0]
    return {start_1: [graph[0, 2], graph[0, 1], graph[0, 0]],
            start_2: [graph[2, 0], graph[1, 0], graph[0, 0]]}


def test_bfs_non_shared(paths_true: dict[Node, list[Node]]) -> None:
    """
    ========================================================================
     Test BFS-Algorithm with non-shared State.
    ========================================================================
    """
    algo = GenAlgoManyToOne.gen_3x3_bfs(is_shared=False)
    sol = algo.run()
    assert sol
    assert sol.paths == paths_true
    assert sol.generated == 14
    assert sol.explored == 8


def test_bfs_shared(paths_true: dict[Node, list[Node]]) -> None:
    """
    ========================================================================
     Test BFS-Algorithm with shared State.
    ========================================================================
    """
    algo = GenAlgoManyToOne.gen_3x3_bfs(is_shared=True)
    sol = algo.run()
    assert sol
    assert sol.paths == paths_true
    assert sol.generated == 14
    assert sol.explored == 8


def test_astar_non_shared(paths_true: dict[Node, list[Node]]) -> None:
    """
    ========================================================================
     Test A*-Algorithm with non-shared State.
    ========================================================================
    """
    algo = GenAlgoManyToOne.gen_3x3_astar(is_shared=False)
    sol = algo.run()
    assert sol
    assert sol.paths == paths_true
    assert sol.generated == 10
    assert sol.explored == 4


def test_astar_shared(paths_true: dict[Node, list[Node]]) -> None:
    """
    ========================================================================
     Test A*-Algorithm with shared State.
    ========================================================================
    """
    algo = GenAlgoManyToOne.gen_3x3_astar(is_shared=True)
    sol = algo.run()
    assert sol
    assert sol.paths == paths_true
    assert sol.generated == 10
    assert sol.explored == 4
