from f_gui.layout.bounds._factory import FactoryBounds
from f_gui.layout.bounds.bounds import Bounds
from f_gui.layout.rect._factory import FactoryRect


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
    bounds = FactoryBounds.half()
    assert bounds.absolute == FactoryRect.half()


def test_quarter():
    """
    ========================================================================
     Test the quarter layout.
    ========================================================================
    """
    bounds = FactoryBounds.quarter()
    assert bounds.absolute == FactoryRect.quarter()
