from f_gui.geometry.generators.g_position import GenPosition
from f_gui.geometry.generators.g_tlwh import GenTLWH


def test_half():
    """
    ========================================================================
     Test the half position.
    ========================================================================
    """
    position = GenPosition.gen_position_half()
    assert position.parent == GenTLWH.full()
    assert position.relative == GenTLWH.half()
    assert position.absolute == GenTLWH.half()


def test_quarter():
    """
    ========================================================================
     Test the quarter position.
    ========================================================================
    """
    position = GenPosition.gen_position_quarter()
    assert position.parent == GenTLWH.half()
    assert position.relative == GenTLWH.quarter()
    assert position.absolute == GenTLWH.quarter()
