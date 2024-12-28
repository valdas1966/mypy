from f_graph.path.single.algos.bfs import BFS
from f_graph.path.single.problem import ProblemSingle
from f_graph.path.cache.i_1_explored import CacheExplored


problem = ProblemSingle.gen_3x3()
graph = problem.graph.clone()
graph[1, 2].parent = graph[2, 2]
explored = {graph[1, 2], graph[2, 2]}
cache = CacheExplored(explored=explored)
bfs = BFS(problem=problem, cache=cache)
solution = bfs.run()
print(explored)
print(solution.path)
#assert solution.path == [graph[0, 0], graph[0, 1], graph[0, 2],
#                         graph[1, 2], graph[2, 2]]
#assert solution.state.explored == {graph[0, 0], graph[0, 1], graph[0, 2],
#                                   graph[1, 0], graph[1, 1], graph[2, 0]}
#assert set(solution.state.generated) == {graph[2, 1]}
#assert solution.state.best == graph[1, 2]
