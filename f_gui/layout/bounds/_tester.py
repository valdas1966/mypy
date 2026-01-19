from f_gui.layout.bounds.main import Bounds, Rect


def test_full():
    """
    ========================================================================
     Test the full layout.
    ========================================================================
    """
    bounds = Bounds()
    assert bounds.absolute == (0, 0, 100, 100)


def test_half():
    """
    ========================================================================
     Test the half layout.
    ========================================================================
    """
    bounds = Bounds.Factory.half()
    assert bounds.absolute == Rect.Factory.half()


def test_quarter():
    """
    ========================================================================
     Test the quarter layout.
    ========================================================================
    """
    bounds = Bounds.Factory.quarter()
    assert bounds.absolute == Rect.Factory.quarter()
