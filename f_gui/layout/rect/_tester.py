from f_gui.layout.rect._factory import FactoryRect


def test_full():
    """
    ========================================================================
     Test the Full LTWH.
    ========================================================================
    """
    full = FactoryRect.full()
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
    half = FactoryRect.half()
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
    quarter = FactoryRect.quarter()
    assert quarter.top == 37.5
    assert quarter.left == 37.5
    assert quarter.width == 25
    assert quarter.height == 25
