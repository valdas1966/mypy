from f_graph.path.one_to_one.generators.g_algo import GenAlgoOneToOne
from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne


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
    assert sol
    assert sol.path == [graph[0, 0], graph[0, 1], graph[0, 2],
                        graph[1, 2], graph[2, 2]]
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
    assert sol
    assert sol.path == [graph[0, 0], graph[0, 1], graph[0, 2],
                        graph[1, 2], graph[2, 2]]
    assert sol.stats.generated == 7
    assert sol.stats.explored == 4
