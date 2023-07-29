from f_data_structure.inner.xy.i_0_init import XYInit


def test_init_default():
    xy = XYInit(x=1, y=2)
    assert xy.x == 1
    assert xy.y == 2
    assert xy.name is None


def test_init_not_default():
    xy = XYInit(x=1, y=2, name='a')
    assert xy.x == 1
    assert xy.y == 2
    assert xy.name == 'a'


def test_str():
    xy_1 = XYInit(x=1, y=2)
    xy_2 = XYInit(x=1, y=2, name='A')
    assert str(xy_1) == '(1,2)'
    assert str(xy_2) == 'A(1,2)'


def test_eq():
    xy_1 = XYInit(x=1, y=1)
    xy_2 = XYInit(x=1, y=1)
    xy_3 = XYInit(x=3, y=3)
    assert xy_1 == xy_2
    assert not xy_1 == xy_3
