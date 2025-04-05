from f_psl.math.u_multiple import UMultiple


def test_nearest() -> None:
    """
    ========================================================================
     Test the nearest() function.
    ========================================================================
    """
    assert UMultiple.nearest(n=0, mult=4) == 0
    assert UMultiple.nearest(n=1, mult=4) == 0
    assert UMultiple.nearest(n=2, mult=4) == 4
    assert UMultiple.nearest(n=3, mult=4) == 4
    assert UMultiple.nearest(n=4, mult=4) == 4
    
    