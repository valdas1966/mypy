from f_math.shapes import Rect


def test_full():
    """
    ========================================================================
     Test the Full LTWH.
    ========================================================================
    """
    full = Rect.Factory.full()
    assert full.top == 0
    assert full.left == 0
    assert full.width == 100
    assert full.height == 100


def test_half():
    """
    ========================================================================
     Test the Half LTWH.
    ========================================================================
    """
    half = Rect.Factory.half()
    assert half.top == 25
    assert half.left == 25
    assert half.width == 50
    assert half.height == 50


def test_quarter():
    """
    ========================================================================
     Test the Quarter LTWH.
    ========================================================================
    """ 
    quarter = Rect.Factory.quarter()
    assert quarter.top == 37.5
    assert quarter.left == 37.5
    assert quarter.width == 25
    assert quarter.height == 25


def test_to_min_max():
    """
    ========================================================================
     Test the to min max method.
    ========================================================================
    """
    rect = Rect.Factory.full()
    assert rect.to_min_max() == (0, 0, 100, 100)


def test_from_center():
    """
    ========================================================================
     Test the from center method.
    ========================================================================
    """
    rect = Rect.From.Center(x=50, y=50, distance=25)
    assert rect.top == 25
    assert rect.left == 25
    assert rect.width == 51
    assert rect.height == 51
