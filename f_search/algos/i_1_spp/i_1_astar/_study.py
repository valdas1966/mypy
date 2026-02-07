from f_search.algos.i_1_spp.i_1_astar import AStar


astar = AStar.Factory.without_obstacles()
astar._verbose = True
solution = astar.run()
