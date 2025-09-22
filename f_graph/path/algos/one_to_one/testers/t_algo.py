from f_graph.path.algos.one_to_one.generators.g_algo import GenAlgoOneToOne
from f_graph.path.algos.one_to_one.generators.g_problem import GenProblemOneToOne
from f_hs.ds.path import Path


def test_bfs():
    """
    ========================================================================
     Test BFS-Algorithm.
    ========================================================================
    """
    problem = GenProblemOneToOne.gen_3x3()
    graph = problem.graph
    algo = GenAlgoOneToOne.gen_3x3_bfs()
    sol = algo.run()
    nodes = [graph[0, 0], graph[0, 1], graph[0, 2], graph[1, 2], graph[2, 2]]
    path_true = Path.from_list(nodes=nodes)
    assert sol
    assert sol.path == path_true
    assert sol.stats.generated == 9
    assert sol.stats.explored == 8


def test_astar():
    """
    ========================================================================
     Test A*-Algorithm.
    ========================================================================
    """
    problem = GenProblemOneToOne.gen_3x3()
    graph = problem.graph
    algo = GenAlgoOneToOne.gen_3x3_astar()
    sol = algo.run()
    nodes = [graph[0, 0], graph[0, 1], graph[0, 2], graph[1, 2], graph[2, 2]]
    path_true = Path.from_list(nodes=nodes)
    assert sol
    assert sol.path == path_true
    assert sol.stats.generated == 7
    assert sol.stats.explored == 4
