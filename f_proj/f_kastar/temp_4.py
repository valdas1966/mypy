from f_astar.c_astar import AStar
from f_grid import u_grid

li_1 = [0,1,2,-1,4]
li_2 = [-1,6,7,-1,9]
li_3 = [10,11,12,13,14]
li_4 = [15,16,17,-1,19]
li_5 = [20,-1,22,23,24]

li = [li_1, li_2, li_3, li_4, li_5]

grid = u_grid.lists_to_grid(li)
start = 1
goal_1 = 12
goal_2 = 9

astar = AStar(grid, start, goal_1)
astar.run()
astar.run(goal_2)
print(astar.get_path())
