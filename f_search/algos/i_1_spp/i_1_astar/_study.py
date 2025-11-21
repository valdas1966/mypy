from f_search.algos.i_1_spp.i_1_astar import AStar
from f_search.ds import StateBase


astar = AStar.Factory.with_obstacles()
solution = astar.run()

print(type(solution))
print(type(solution.stats))
print(type(solution.stats.elapsed))