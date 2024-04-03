from f_heuristic_search.problem_types.spp.i_0_concrete import SPPConcrete
from f_heuristic_search.algos.spp.i_1_bfs import BFS
from f_data_structure.graphs.i_1_grid import GraphGrid as Graph


graph = Graph.from_shape(rows=3)
start = graph[0][0]
goal = graph[2][2]
spp = SPPConcrete(graph=graph, start=start, goal=goal)
bfs = BFS(spp=spp)
bfs.run()
print(bfs.is_path_found)
print(bfs.optimal_path())
print(sorted(bfs.expanded))
