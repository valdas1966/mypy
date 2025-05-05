from f_math.u_interpolation import UInterpolation


def test_linear():
    """
    ===========================================================================
     Test the linear() interpolation function.
    ===========================================================================
    """
    # Start-Point
    assert UInterpolation.linear(a=2, b=4, t=0.0) == 2.0
    # 1/4-Point
    assert UInterpolation.linear(a=2, b=4, t=0.25) == 2.5
    # Mid-Point
    assert UInterpolation.linear(a=2, b=4, t=0.5) == 3.0
    # Finish-Point
    assert UInterpolation.linear(a=2, b=4, t=1.0) == 4.0


def test_linear_list():
    """
    ===========================================================================
     Test the linear_list() interpolation function.
    ===========================================================================
    """
    # Test with 3 steps.
    assert UInterpolation.linear_list(a=2, b=4, n=3) == [2, 3, 4]
    # Test with 5 steps.
    assert UInterpolation.linear_list(a=2, b=4, n=5) == [2, 2.5, 3, 3.5, 4]

