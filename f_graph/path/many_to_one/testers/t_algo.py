from f_graph.path.many_to_one.generators.g_problem import GenProblemManyToOne
from f_graph.path.many_to_one.generators.g_algo import GenAlgoManyToOne
from f_graph.path.many_to_one.algo import AlgoManyToOne, TypeAlgo
from f_graph.path.one_to_one.algo import AlgoOneToOne
from f_graph.path.generators.g_graph import GenGraphPath, NodePath as Node
from f_graph.path.path import Path
import pytest


@pytest.fixture
def paths_true() -> dict[Node, Path]:
    """
    ========================================================================
     Fixture for the paths of the 3x3-Grid-Problem.
    ========================================================================
    """
    graph = GenGraphPath.gen_3x3()
    start_1 = graph[0, 2]
    start_2 = graph[2, 2]
    nodes_1 = [graph[0, 2], graph[0, 1], graph[0, 0]]
    nodes_2 = [graph[2, 2], graph[1, 2], graph[0, 2], graph[0, 1], graph[0, 0]]
    path_1 = Path.from_list(nodes=nodes_1)
    path_2 = Path.from_list(nodes=nodes_2)
    return {start_1: path_1, start_2: path_2}


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
    assert sol.generated == 17
    assert sol.explored == 13


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
    assert sol.generated == 12
    assert sol.explored == 6


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


def test_3_starts() -> None:
    """
    ========================================================================
     Test the 3-starts problem.
    ========================================================================
    """
    problem = GenProblemManyToOne.gen_3x3x3()
    algo = AlgoManyToOne(problem=problem,
                         type_algo=TypeAlgo.A_STAR,
                         is_shared=True,
                         with_boundary=True)
    solution = algo.run()
    assert solution
    for p in problem.to_singles():
        algo_oto = AlgoOneToOne(problem=p, type_algo=TypeAlgo.A_STAR)
        solution_oto = algo_oto.run()
        assert solution_oto.path == solution.paths[p.start]
    
