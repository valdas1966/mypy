from f_data_structure.mixins.has_row_col import HasRowCol


def test_str():
    rc = HasRowCol(1, 2)
    assert str(rc) == '(1,2)'
    rc = HasRowCol(3)
    assert str(rc) == '(3,3)'
    rc = HasRowCol()
    assert str(rc) == '(0,0)'


def test_comparison():
    assert HasRowCol(0, 0) < HasRowCol(0, 1) < HasRowCol(1, 0) < HasRowCol(1, 1)
