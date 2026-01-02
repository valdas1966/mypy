from f_search.algos.i_2_omspp.i_1_iterative import IterativeOMSPP


algo = IterativeOMSPP.Factory.without_obstacles_4x4()
solution = algo.run()
for goal, sub_solution in solution.subs.items():
    print(goal, sub_solution.stats)

