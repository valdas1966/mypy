from f_gui.components.generators.g_position import GenPosition
from f_gui.components.generators.g_tlwh import GenLTWH


def test_half():
    """
    ========================================================================
     Test the half position.
    ========================================================================
    """
    position = GenPosition.gen_position_half()
    assert position.parent == GenLTWH.full()
    assert position.relative == GenLTWH.half()
    assert position.absolute == GenLTWH.half()


def test_quarter():
    """
    ========================================================================
     Test the quarter position.
    ========================================================================
    """
    position = GenPosition.gen_position_quarter()
    assert position.parent == GenLTWH.half()
    assert position.relative == GenLTWH.half()
    assert position.absolute == GenLTWH.quarter()
