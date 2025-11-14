from f_search.algos.i_1_oospp.i_1_astar import AStar
from f_search.ds import State


astar = AStar.Factory.with_obstacles()
astar.run()
for state in astar._explored:
    print(state.key)
grid = astar._problem.grid
state_10 = State(grid[1][0])
state_21 = State(grid[2][1])
print(astar._cost[state_10].key_comparison())
print(astar._cost[state_21].key_comparison())
print(astar._counters['UPDATED'])
