from f_utils.dtypes.u_int import UInt as u_int


def test_rel_to_abs():
    rel = 50
    total = 80
    assert u_int.rel_to_abs(rel, total) == 40


def test_dims_rel_to_abs():
    total_width = 200
    total_height = 200
    x = 50
    y = 80
    width = 20
    height = 10
    res = u_int.dims_rel_to_abs(x, y, width, height, total_width, total_height)
    assert res == (100, 160, 40, 20)
