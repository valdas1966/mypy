from f_gui.geometry.generators.g_position import GenPosition
from f_gui.geometry.generators.g_bounds import GenBounds


def test_half():
    """
    ========================================================================
     Test the half position.
    ========================================================================
    """
    position = GenPosition.gen_position_half()
    assert position.absolute == GenBounds.half()


def test_quarter():
    """
    ========================================================================
     Test the quarter position.
    ========================================================================
    """
    position = GenPosition.gen_position_quarter()
    assert position.absolute == GenBounds.quarter()
