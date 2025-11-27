from f_search.algos import KDijkstra


algo = KDijkstra.Factory.with_obstacles()
solution = algo.run()
goal_1, goal_2 = algo._problem.goals
path_1 = solution.paths[goal_1]
path_2 = solution.paths[goal_2]

#print(path_1)

