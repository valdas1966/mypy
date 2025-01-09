from f_graph.path.single.algos.a_star import AStar, Problem
from f_graph.path.graph import GraphPath, NodePath
from f_graph.path.cache.i_1_explored import CacheExplored


def test_a_star():
    problem = Problem.gen_3x3()
    graph = problem.graph
    astar = AStar(problem=problem)
    solution = astar.run()
    assert solution.path == [graph[0, 0], graph[0, 1], graph[0, 2],
                             graph[1, 2], graph[2, 2]]
    assert solution.state.explored == {graph[0, 0], graph[0, 1],
                                       graph[0, 2], graph[1, 2]}
    assert set(solution.state.generated) == {graph[1, 0], graph[1, 1]}
    assert solution.state.best == problem.goal


def test_a_star_cache():
    graph = GraphPath.gen_3x3(type_node=NodePath)
    problem_a = Problem(graph=graph, start=graph[2, 2], goal=graph[0, 2])
    astar_a = AStar(problem=problem_a, name='Backward')
    solution_a = astar_a.run()
    problem_b = Problem.gen_3x3()
    cache_b = CacheExplored(explored=solution_a.state.explored)
    astar_b = AStar(problem=problem_b, cache=cache_b, name='Forward')
    solution_b = astar_b.run()
    assert solution_b.path == [graph[0, 0], graph[0, 1], graph[0, 2],
                               graph[1, 2], graph[2, 2]]
    assert solution_b.state.explored == {graph[0, 0], graph[0, 1], graph[0, 2]}
    assert solution_b.state.best == graph[1, 2]
