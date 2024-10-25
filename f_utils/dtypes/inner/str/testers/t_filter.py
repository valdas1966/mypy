from f_utils.dtypes.inner.str.filter import Filter


def test_specific_chars():
    s = 'a,b'
    chars = {','}
    answer = Filter.specific_chars(s=s, chars=chars)
    expected = 'ab'
    assert answer == expected
