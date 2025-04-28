from f_graph.path.one_to_many.generators.g_algo import GenAlgoOneToMany
from f_graph.path.one_to_many.generators.g_problem import GenProblemOneToMany
from f_graph.path.node import NodePath as Node
from f_graph.path.path import Path
import pytest


@pytest.fixture
def paths_true() -> dict[Node, list[Node]]:
    """
    ========================================================================
     True Paths for the 3x3 Graph.
    ========================================================================
    """
    problem = GenProblemOneToMany.gen_3x3()
    graph = problem.graph
    paths = dict()
    paths[graph[0, 2]] = Path([graph[0, 0], graph[0, 1], graph[0, 2]])
    paths[graph[2, 0]] = Path([graph[0, 0], graph[1, 0], graph[2, 0]])
    return paths


def test_bfs_shared(paths_true) -> None:
    """
    ========================================================================
     Test the BFS Algorithm with Shared-Data.
    ========================================================================
    """
    algo = GenAlgoOneToMany.gen_bfs_shared()
    solution = algo.run()
    assert solution
    assert solution.paths == paths_true
    assert solution.generated == 8
    assert solution.explored == 5


def test_bfs_not_shared(paths_true) -> None:
    """
    ========================================================================
    Test the BFS Algorithm with Not Shared-Data.
    ========================================================================
    """
    algo = GenAlgoOneToMany.gen_bfs_not_shared()
    solution = algo.run()
    assert solution
    assert solution.paths == paths_true
    assert solution.generated == 14
    assert solution.explored == 8


def test_a_star_shared(paths_true) -> None:
    """
    ========================================================================
     Test the A* Algorithm with Shared-Data.
    ========================================================================
    """
    algo = GenAlgoOneToMany.gen_astar_shared()
    solution = algo.run()
    assert solution
    assert solution.paths == paths_true
    assert solution.generated == 6
    assert solution.explored == 3


def test_a_star_not_shared(paths_true) -> None:
    """
    ========================================================================
     Test the A* Algorithm with Not Shared-Data.
    ========================================================================
    """ 
    algo = GenAlgoOneToMany.gen_astar_not_shared()
    solution = algo.run()
    assert solution
    assert solution.paths == paths_true
    assert solution.generated == 10
    assert solution.explored == 4
