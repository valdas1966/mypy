from f_ds.grids.generators.g_grid import GenGrid, Cell
from f_graph.path.graph import GraphPath
from f_graph.path.many_to_one.problem import ProblemManyToOne
from f_graph.path.many_to_one.algo import AlgoManyToOne, AlgoOneToOne
from f_graph.path.cache import Cache
from f_graph.path.boundary import Boundary


# Create a grid
grid = GenGrid.gen_random(rows=4, pct_invalid=0)
# Add obstacles
obstacles = [grid[1][1], grid[2][2]]
Cell.invalidate(obstacles)
# Create a graph
graph = GraphPath(grid=grid)
# Create starts
start_1 = graph[2, 0]
start_2 = graph[3, 2]
starts = [start_1, start_2]
# Create a goal
goal = graph[1, 2]
# Create problems
problem = ProblemManyToOne(graph=graph, starts=starts, goal=goal)
problem_with = problem.clone()
problem_without = problem.clone()
# Run the algorithm without boundary
algo_without = AlgoManyToOne(problem=problem_without, with_boundary=False)
sol_without = algo_without.run()
print(f'{len(sol_without.states[start_1].explored)}'
      f' + {len(sol_without.states[start_2].explored)} = {sol_without.explored}')
# Run the algorithm with boundary
algo_with = AlgoManyToOne(problem=problem_with, with_boundary=True)
sol_with = algo_with.run()
print(f'{len(sol_with.states[start_1].explored)}'
      f' + {len(sol_with.states[start_2].explored)} = {sol_with.explored}')
print([node for node in sol_with.states[start_2].explored])
"""
problem_1, problem_2 = problem_with.to_singles()
algo_1 = AlgoOneToOne(problem=problem_1)
sol_1 = algo_1.run()
path_1 = sol_1.path
print(sol_1.stats.explored)
print(path_1)
cache = Cache.from_path(path=path_1)
boundary = Boundary.from_path(path=path_1, graph=graph, cache=cache)
print()
print()
print()
print('Start 2')
print()
print()
print()
algo_2 = AlgoOneToOne(problem=problem_2, cache=cache, boundary=boundary)
sol_2 = algo_2.run()
explored_with = sol_with.states[start_2].explored
explored_without = sol_without.states[start_2].explored
"""