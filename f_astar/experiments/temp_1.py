from f_astar.c_astar import AStar
from f_astar.c_astar_lookup import AStarLookup
from f_grid import u_gen_grid

grid = u_gen_grid.random(4)
start = 0
goal_near = 4
goal_far = 12
astar = AStar(grid, start, goal_near)
astar.run()
expanded_near = len(astar.closed)
print([node.idd for node in astar.closed])
lookup = astar.closed.copy()
astar.run(goal_far)
forward = len(astar.closed) - expanded_near
print([node.idd for node in astar.closed])
astar_lookup = AStarLookup(grid, goal_far, start, closed=lookup)
astar_lookup.run()
backward = len(astar_lookup.closed)
print([node.idd for node in astar_lookup.closed])
print(expanded_near, forward, backward)
