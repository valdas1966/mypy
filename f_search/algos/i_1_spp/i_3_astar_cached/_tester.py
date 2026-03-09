from f_search.algos.i_1_spp.i_3_astar_cached import AStarCached
from f_search.algos.i_1_spp.i_1_astar import AStar
from f_search.problems import ProblemSPP


def test_without_cache() -> None:
    algo = AStarCached.Factory.without_cache()
    sol = algo.run()
    assert sol.stats.explored == 22


def test_with_cache() -> None:
    algo = AStarCached.Factory.with_cache()
    sol = algo.run()
    assert sol.stats.explored == 10


def test_with_bounded() -> None:
    algo = AStarCached.Factory.with_bounded()
    sol = algo.run()
    assert sol.stats.explored == 8


def test_with_bounded_depth_1() -> None:
    algo = AStarCached.Factory.with_bounded_depth_1()
    sol = algo.run()
    assert sol.stats.explored == 5


def test_with_bounded_depth_2() -> None:
    algo = AStarCached.Factory.with_bounded_depth_2()
    sol = algo.run()
    assert sol.stats.explored == 4


def test_quality_h() -> None:
    """
    ========================================================================
     Test quality_h is consistent across all cache variants.
    ========================================================================
    """
    names_factory = ['without_cache',
                     'with_cache',
                     'with_bounded',
                     'with_bounded_depth_1',
                     'with_bounded_depth_2']
    expected = 5 / 13
    for name in names_factory:
        algo = getattr(AStarCached.Factory, name)()
        sol = algo.run()
        assert sol.quality_h == expected
