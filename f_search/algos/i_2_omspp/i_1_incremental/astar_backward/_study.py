from f_search.algos.i_2_omspp.i_1_incremental import AStarIncrementalBackward
from f_search.problems.i_2_omspp import ProblemOMSPP


problem = ProblemOMSPP.Factory.for_cached()
algo = AStarIncrementalBackward(problem=problem, depth_propagation=0)
sol = algo.run()
for state in algo.list_explored():
    print(state)
