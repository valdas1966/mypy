from f_ds.grids.generators.g_grid import GenGrid, Cell
from f_graph.path.graph import GraphPath
from f_graph.path.many_to_one.problem import ProblemManyToOne
from f_graph.path.many_to_one.algo import AlgoManyToOne, AlgoOneToOne
from f_graph.path.cache import Cache
from f_graph.path.boundary import Boundary


# Create a grid
grid = GenGrid.gen_random(rows=5, pct_invalid=0)
# Add obstacles
obstacles = [grid[3][3], grid[4][2]]
Cell.invalidate(obstacles)
# Create a graph
graph = GraphPath(grid=grid)
# Create starts
start_1 = graph[1, 1]
start_2 = graph[2, 0]
starts = [start_1, start_2]
# Create a goal
goal = graph[4, 3]
# Create problems
problem = ProblemManyToOne(graph=graph, starts=starts, goal=goal)
problem_with = problem.clone()
problem_without = problem.clone()
# Run the algorithm without boundary
print('Without:')
algo_without = AlgoManyToOne(problem=problem_without, with_boundary=False)
sol_without = algo_without.run()
print(f'{len(sol_without.states[start_1].explored)}'
      f' + {len(sol_without.states[start_2].explored)} = {sol_without.explored}')

"""
print('Path to S1:')
print(sol_without.paths[start_1])
print('Explored Without:')
for node in sorted(sol_without.states[start_2].explored):
      node.print_details()
print('Generated Without:')
for node in sorted(sol_without.states[start_2].generated):
      node.print_details()
print('Best Without:')
print(sol_without.states[start_2].best.print_details())
"""

# Run the algorithm with boundary
print('With:')
algo_with = AlgoManyToOne(problem=problem_with, with_boundary=True)
sol_with = algo_with.run()
print(f'{len(sol_with.states[start_1].explored)}'
      f' + {len(sol_with.states[start_2].explored)} = {sol_with.explored}')

"""
print('Explored With:')
for node in sorted(sol_with.states[start_2].explored):
      node.print_details()
print('Generated With:')
for node in sorted(sol_with.states[start_2].generated):
      node.print_details()
print('Best With:')
print(sol_with.states[start_2].best.print_details())
"""