from f_search.algos.i_2_omspp import AStarAggregative, AStarIncremental, DijkstraIncremental
from f_search.problems.i_2_omspp.main import ProblemOMSPP


def compare() -> None:
    problem = ProblemOMSPP.Factory.all_goals(rows=150)
    dijkstra = DijkstraIncremental(problem=problem)
    stats_dijkstra = dijkstra.run().stats
    print(stats_dijkstra)
    inc = AStarIncremental(problem=problem)
    stats_inc = inc.run().stats
    print(stats_inc)
    #agg = AStarAggregative(problem=problem)
    #stats_agg = agg.run().stats
    #print(stats_agg)


compare()
