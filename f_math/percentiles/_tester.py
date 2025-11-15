from f_math.percentiles.main import UPercentiles


def test_get_percentile_bins() -> None:
    """
    ========================================================================
     Test the get_percentile_bins() method.
    ========================================================================
    """
    values = [1, 2, 3, 4]
    n_bins = 50
    actual = UPercentiles.get_percentile_bins(values=values, n_bins=n_bins)
    expected = [(1, 3), (3, 5)]
    assert actual == expected
