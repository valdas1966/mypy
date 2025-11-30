from f_search.stats import StatsSearch


def test_stats_search():
    """
    ========================================================================
     Test the StatsSearch class.
    ========================================================================
    """
    stats = StatsSearch.Factory.linear()
    assert stats.elapsed == 0
    assert stats.generated == 10
    assert stats.explored == 20
