from f_gui.geometry.generators.g_geometry import GenGeometry, Geometry
from f_gui.geometry.generators.g_bounds import GenBounds


def test_full():
    """
    ========================================================================
     Test the full geometry.
    ========================================================================
    """
    geometry = Geometry()
    assert geometry.bounds_absolute == (0, 0, 100, 100)


def test_half():
    """
    ========================================================================
     Test the half geometry.
    ========================================================================
    """
    geometry = GenGeometry.half()
    assert geometry.bounds_absolute == GenBounds.half()


def test_quarter():
    """
    ========================================================================
     Test the quarter geometry.
    ========================================================================
    """
    geometry = GenGeometry.quarter()
    assert geometry.bounds_absolute == GenBounds.quarter()
