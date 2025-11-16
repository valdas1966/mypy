from f_search.algos.i_1_omspp.i_1_kx_astar import Factory


def test_without_obstacles():
    algo = Factory.without_obstacles()
    solution = algo.run()
    assert solution.stats.explored == 8

