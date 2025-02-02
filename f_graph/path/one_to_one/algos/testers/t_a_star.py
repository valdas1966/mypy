from f_graph.path.one_to_one.algos.a_star import AStar
from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne
from f_graph.path.one_to_one.generators.g_cache import GenCache


def test_a_star():
    problem = GenProblemOneToOne.gen_3x3()
    astar = AStar(problem=problem)
    solution = astar.run()
    graph = problem.graph
    assert solution.path == [graph[0, 0], graph[0, 1], graph[0, 2],
                             graph[1, 2], graph[2, 2]]
    assert solution.state.explored == {graph[0, 0], graph[0, 1],
                                       graph[0, 2], graph[1, 2]}
    assert set(solution.state.generated) == {graph[1, 0], graph[1, 1]}
    assert solution.state.best == problem.goal


def test_a_star_cache():
    problem = GenProblemOneToOne.gen_3x3()
    cache = GenCache.gen_3x3()
    astar = AStar(problem=problem, cache=cache)
    solution = astar.run()
    graph = problem.graph
    assert solution.path == [graph[0, 0], graph[0, 1], graph[0, 2],
                             graph[1, 2], graph[2, 2]]
    assert solution.state.explored == {graph[0, 0], graph[0, 1], graph[0, 2]}
    assert set(solution.state.generated) == {graph[1, 0], graph[1, 1]}
    assert solution.state.best == problem.pre_goal
