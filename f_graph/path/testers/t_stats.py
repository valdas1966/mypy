from f_graph.path.stats import StatsPath


def test_stats_path_init() -> None:
    """
    ============================================================================
     Test that StatsPath initializes with correct elapsed time and explored count.
    ============================================================================
    """
    stats = StatsPath(elapsed=10, explored=5)
    assert stats.elapsed == 10
    assert stats.explored == 5


def test_stats_path_properties() -> None:
    """
    ============================================================================
     Test that StatsPath properties return correct values.
    ============================================================================
    """
    stats = StatsPath(elapsed=20, explored=15)
    
    # Test elapsed property
    assert isinstance(stats.elapsed, int)
    assert stats.elapsed == 20
    
    # Test explored property 
    assert isinstance(stats.explored, int)
    assert stats.explored == 15
