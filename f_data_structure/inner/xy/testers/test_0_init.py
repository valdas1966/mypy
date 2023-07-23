from f_data_structure.inner.xy.i_0_init import XYInit


def test_init():
    xy = XYInit(x=1, y=2)
    assert xy.x == 1
    assert xy.y == 2


def test_str():
    xy = XYInit(x=1, y=2)
    assert str(xy) == '(1,2)'


def test_eq():
    xy_1 = XYInit(x=1, y=1)
    xy_2 = XYInit(x=1, y=1)
    xy_3 = XYInit(x=3, y=3)
    assert xy_1 == xy_2
    assert not xy_1 == xy_3
