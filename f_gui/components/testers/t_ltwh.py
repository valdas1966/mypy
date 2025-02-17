from f_gui.components.generators.g_ltwh import GenLTWH


def test_ltwh():
    """
    ========================================================================
     Test the LTWH class.
    ========================================================================
    """
    full = GenLTWH.gen_ltwh_full()
    assert full.left == 0
    assert full.top == 0
    assert full.width == 100
    assert full.height == 100
    
    half = GenLTWH.gen_ltwh_half()
    assert half.left == 25
    assert half.top == 25
    assert half.width == 50
    assert half.height == 50
