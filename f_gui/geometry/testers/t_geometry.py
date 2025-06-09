from f_gui.geometry.generators.g_geometry import GenGeometry
from f_gui.geometry.generators.g_bounds import GenBounds


def test_half():
    """
    ========================================================================
     Test the half geometry.
    ========================================================================
    """
    geometry = GenGeometry.gen_geometry_half()
    assert geometry.absolute == GenBounds.half()


def test_quarter():
    """
    ========================================================================
     Test the quarter geometry.
    ========================================================================
    """
    geometry = GenGeometry.gen_geometry_quarter()
    assert geometry.absolute == GenBounds.quarter()
