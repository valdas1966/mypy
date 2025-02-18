from f_gui.components.generators.g_position import GenPosition
from f_gui.components.generators.g_ltwh import GenLTWH


def test_half():
    """
    ========================================================================
     Test the half position.
    ========================================================================
    """
    position = GenPosition.gen_position_half()
    assert position.relative == GenLTWH.gen_ltwh_half()
    #assert position.absolute == GenLTWH.gen_ltwh_half()


def test_quarter():
    """
    ========================================================================
     Test the quarter position.
    ========================================================================
    """
    position = GenPosition.gen_position_quarter()
    assert position.relative == GenLTWH.gen_ltwh_quarter()
    assert position.absolute == GenLTWH.gen_ltwh_quarter()
