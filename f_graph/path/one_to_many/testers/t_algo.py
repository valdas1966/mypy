from f_graph.path.one_to_many.generators.g_algo import GenAlgoOneToMany
from f_graph.path.one_to_many.generators.g_problem import GenProblemOneToMany


def test_bfs_shared() -> None:
    """
    ========================================================================
     Test the BFS Algorithm with Shared-Data.
    ========================================================================
    """
    problem = GenProblemOneToMany.gen_3x3()
    graph = problem.graph
    algo = GenAlgoOneToMany.gen_bfs_shared()
    solution = algo.run()
    assert solution
    assert solution.paths[graph[0, 2]] == [graph[0, 0], graph[0, 1], graph[0, 2]]
