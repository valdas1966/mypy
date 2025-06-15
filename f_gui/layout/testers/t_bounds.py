from f_gui.layout.generators.g_bounds import GenBounds, Bounds
from f_gui.layout.generators.g_rect import GenRect


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
    bounds = GenBounds.half()
    assert bounds.absolute == GenRect.half()


def test_quarter():
    """
    ========================================================================
     Test the quarter layout.
    ========================================================================
    """
    bounds = GenBounds.quarter()
    assert bounds.absolute == GenRect.quarter()
