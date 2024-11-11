from f_graph.algos.one_to_one.i_2_bfs_cache import BFS_CACHE
from f_graph.search.u_problem import UProblemOTO


problem_cache = UProblemOTO.gen_3x3()
graph_cache = problem_cache.graph
graph_cache[0, 2].parent = graph_cache[1, 2]
graph_cache[1, 2].parent = graph_cache[2, 2]
cache = {graph_cache[2, 2]: graph_cache[2, 2].path_from_start}
problem = UProblemOTO.gen_3x3()
graph = problem.graph
bfs = BFS_CACHE(problem=problem, cache=cache)
for node in bfs.get_path():
    print(node)

