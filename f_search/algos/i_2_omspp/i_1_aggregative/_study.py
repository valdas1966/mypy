from f_search.algos.i_2_omspp.i_1_aggregative import AStarAggregative


algo = AStarAggregative.Factory.without_obstacles()
solution = algo.run()
print(bool(solution))
print(all(sub for sub in solution.subs))
print(len(solution.subs))
print(len(solution.problem.goals))
