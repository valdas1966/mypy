from f_math.percentiles.bin.main import Bin
from f_math.percentiles.utils import UPercentiles


def test_get_percentile_bins() -> None:
    """
    ========================================================================
     Test the get_percentile_bins() method.
    ========================================================================
    """
    values = [1, 2, 3, 4]
    n_bins = 50
    actual = UPercentiles.get_bins(values=values, n_bins=n_bins)
    expected = [Bin(percentile=50, lower=1, upper=6),
                Bin(percentile=100, lower=6, upper=11)]
    assert actual == expected
