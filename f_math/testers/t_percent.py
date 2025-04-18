from f_math.u_percent import UPercent


def test_to_pct() -> None:
    """
    ========================================================================
     Test the to_pct() method.
    ========================================================================
    """
    vals = [1, 2, 3]
    actual = UPercent.to_pct(vals)
    expected = [17, 33, 50]
    assert actual == expected


def test_pct_of() -> None:
    """
    ========================================================================
     Test the pct_of() method.
    ========================================================================
    """
    assert UPercent.pct_of(a=1, b=2) == 50
    assert UPercent.pct_of(a=1, b=2, precision=1) == 50.0
    assert UPercent.pct_of(a=1, b=3, precision=2) == 33.33

