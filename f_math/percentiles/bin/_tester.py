from f_math.percentiles.bin import Bin


def test_contains() -> None:
    """
    ========================================================================
     Test the contains method.
    ========================================================================
    """
    bin = Bin(percentile=10, lower=0, upper=10)
    assert 0 in bin
    assert 5 in bin
    assert 10 not in bin
    

def test_repr() -> None:
    """
    ========================================================================
     Test the repr method.
    ========================================================================
    """
    bin = Bin(percentile=10, lower=0, upper=10)
    assert repr(bin) == "Bin(percentile=10, range=[0, 10))"
