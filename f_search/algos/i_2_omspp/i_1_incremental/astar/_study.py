from f_search.algos.i_2_omspp import AStarIncremental
from f_search.problems.i_2_omspp import ProblemOMSPP


problem = ProblemOMSPP.Factory.all_goals(rows=2)
algo = AStarIncremental(problem=problem)
solution = algo.run()
stats = solution.stats
print(stats)
