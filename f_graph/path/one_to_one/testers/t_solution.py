from f_graph.path.one_to_one.generators.g_solution import GenSolutionOneToOne
from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne


def test_solution_3x3() -> None:
    """
    ========================================================================
     Test that solution_3x3 creates a solution for a 3x3 problem.
    ========================================================================
    """
    solution = GenSolutionOneToOne.gen_3x3()
    problem = GenProblemOneToOne.gen_3x3()
    graph = problem.graph
    path_true = [graph[0, 0], graph[0, 1], graph[0, 2],
                 graph[1, 2], graph[2, 2]]
    assert solution.path == path_true
