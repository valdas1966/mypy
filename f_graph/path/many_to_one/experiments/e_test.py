from f_ds.grids.generators.g_grid import GenGrid, Cell
from f_graph.path.graph import GraphPath
from f_graph.path.many_to_one.problem import ProblemManyToOne
from f_graph.path.many_to_one.algo import AlgoManyToOne, TypeAlgo


grid = GenGrid.gen_random(rows=5, pct_invalid=0)
obstacles = (grid[3][0], grid[2][1], grid[1][1], grid[1][2])
Cell.invalidate(obstacles)
graph = GraphPath(grid=grid)
start_1 = graph[3, 3]
start_2 = graph[2, 2]
starts = {start_1, start_2}
goal = graph[2, 0]
problem = ProblemManyToOne(graph=graph, starts=starts, goal=goal)
algo = AlgoManyToOne(problem=problem,
                      type_algo=TypeAlgo.A_STAR,
                        is_shared=True,
                          is_eager=True,
                            with_boundary=True)
solution = algo.run()
print(solution.stats[start_1].explored)
print(solution.stats[start_2].explored)
print(solution.explored)
