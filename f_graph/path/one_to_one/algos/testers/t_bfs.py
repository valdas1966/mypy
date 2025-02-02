from f_graph.path.one_to_one.algos.bfs import BFS
from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne
from f_graph.path.one_to_one.generators.g_cache import GenCache


def test_bfs():
    problem = GenProblemOneToOne.gen_3x3()
    bfs = BFS(problem=problem)
    solution = bfs.run()
    graph = problem.graph
    assert solution.path == [graph[0, 0], graph[0, 1], graph[0, 2],
                             graph[1, 2], graph[2, 2]]
    assert solution.state.explored == {graph[0, 0], graph[0, 1], graph[0, 2],
                                       graph[1, 0], graph[1, 1], graph[1, 2],
                                       graph[2, 0], graph[2, 1]}
    assert not solution.state.generated
    assert solution.state.best == problem.goal


def test_bfs_cache():
    problem = GenProblemOneToOne.gen_3x3()
    graph = problem.graph.clone()
    cache = GenCache.gen_3x3()
    bfs = BFS(problem=problem, cache=cache)
    solution = bfs.run()
    assert solution.path == [graph[0, 0], graph[0, 1], graph[0, 2],
                             graph[1, 2], graph[2, 2]]
    assert solution.state.explored == {graph[0, 0], graph[0, 1], graph[0, 2],
                                       graph[1, 0], graph[1, 1], graph[2, 0]}
    assert set(solution.state.generated) == {graph[2, 1]}
    assert solution.state.best == graph[1, 2]
