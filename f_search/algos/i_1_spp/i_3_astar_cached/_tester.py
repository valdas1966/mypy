from f_search.algos.i_1_spp.i_3_astar_cached import AStarCached
from f_search.algos.i_1_spp.i_1_astar import AStar
from f_search.problems import ProblemSPP


def test_without_cache() -> None:
    algo = AStarCached.Factory.without_cache()
    sol = algo.run()
    assert sol.stats.explored == 22
