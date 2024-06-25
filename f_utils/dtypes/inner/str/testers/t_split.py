from f_utils.dtypes.inner.str.split import Split


s_empty = str()
s_3 = '123'
s_4 = '1234'
length = 2


def test_by_length():
    assert Split.by_length(s_empty, length) == []
    assert Split.by_length(s_3, length) == ['12', '3']
    assert Split.by_length(s_4, length) == ['12', '34']