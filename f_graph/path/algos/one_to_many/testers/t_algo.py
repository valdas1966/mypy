from f_graph.path.algos.one_to_many.generators.g_algo import GenAlgoOneToMany, AlgoOneToMany
from f_graph.path.algos.one_to_many.generators.g_problem import GenProblemOneToMany
from f_hs.ds._old_node import NodePath as Node
from f_hs.ds.path import Path
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


def test_a_star_corner_3_goals() -> None:
    """
    ========================================================================
     Test the A* Algorithm with Corner 3 Goals.
    ========================================================================
    """
    problem = GenProblemOneToMany.corner_3_goals()
    algo = AlgoOneToMany(problem=problem)
    solution = algo.run()
    graph = problem.graph
    goal_1 = graph[0, 3]
    goal_2 = graph[0, 2]
    goal_3 = graph[1, 3]
    path_1 = Path([graph[0, 0], graph[1, 0], graph[2, 0], graph[3, 0],
                   graph[3, 1], graph[3, 2], graph[2, 2], graph[1, 2],
                   graph[0, 2], graph[0, 3]])
    path_2 = Path([graph[0, 0], graph[1, 0], graph[2, 0], graph[3, 0],
                   graph[3, 1], graph[3, 2], graph[2, 2], graph[1, 2],
                   graph[0, 2]])
    path_3 = Path([graph[0, 0], graph[1, 0], graph[2, 0], graph[3, 0],
                   graph[3, 1], graph[3, 2], graph[2, 2], graph[1, 2],
                   graph[1, 3]])
    paths = {goal_1: path_1, goal_2: path_2, goal_3: path_3}
    assert solution
    assert solution.paths == paths
    assert solution.generated == 14
    assert solution.explored == 9

