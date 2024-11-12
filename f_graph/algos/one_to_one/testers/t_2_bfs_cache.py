from f_graph.algos.one_to_one.i_2_bfs_cache import BFS_CACHE
from f_graph.path_finding.u_problem import UProblemOTO


def test():
    problem_cache = UProblemOTO.gen_3x3()
    graph_cache = problem_cache.graph
    graph_cache[0, 2].parent = graph_cache[1, 2]
    graph_cache[1, 2].parent = graph_cache[2, 2]
    cache = {graph_cache[0, 2], graph_cache[1, 2]}
    problem = UProblemOTO.gen_3x3()
    graph = problem.graph
    bfs = BFS_CACHE(problem=problem, cache=cache)
    assert bfs.get_path() == [graph[0, 0], graph[0, 1], graph[0, 2],
                              graph[1, 2], graph[2, 2]]
    assert len(bfs._data.explored) == 3
