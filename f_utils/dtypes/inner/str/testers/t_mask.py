from f_utils.dtypes.inner.str.mask import Mask


def test_full():
    ex_single = 'abc'
    assert Mask.full(ex_single) == '***'
    ex_multi = 'ab c'
    assert Mask.full(ex_multi) == '** *'
