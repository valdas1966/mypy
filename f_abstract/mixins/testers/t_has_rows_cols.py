from f_abstract.mixins.has_rows_cols import HasRowsCols


def test_init():
    h = HasRowsCols(rows=4, cols=5)
    assert h.rows == 4 and h.cols == 5
    h = HasRowsCols(rows=5)
    assert h.rows == 5 and h.cols == 5


def test_shape():
    h = HasRowsCols(rows=5)
    assert h.shape() == '(5,5)'


def test_is_within():
    h = HasRowsCols(rows=5)
    assert h.is_within(row=2, col=3)
    assert not h.is_within(row=5, col=0)


def test_key_comparison():
    h_1 = HasRowsCols(rows=2)
    h_2 = HasRowsCols(rows=3)
    assert h_1 < h_2
    h_3 = HasRowsCols(rows=1, cols=4)
    assert h_3 < h_1


def test_len():
    h = HasRowsCols(5)
    assert len(h) == 25


def test_str():
    h = HasRowsCols(5)
    assert str(h) == '(5,5)'


def test_repr():
    h = HasRowsCols(5)
    assert repr(h) == '<HasRowsCols: (5,5)>'


def test_hash():
    h_1 = HasRowsCols(rows=1, cols=4)
    h_2 = HasRowsCols(2)
    s = {h_1, h_2}
    assert len(s) == 2
