from f_graph.path.generators.g_stats import GenStatsPath


def test_10x20x30() -> None:
    """
    ========================================================================
     Test that StatsPath initializes with correct elapsed time and correct
       number of generated and explored nodes.
    ========================================================================
    """
    stats = GenStatsPath.gen_10x20x30()
    assert stats.elapsed == 10
    assert stats.generated == 20
    assert stats.explored == 30
