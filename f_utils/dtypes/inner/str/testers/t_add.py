from f_utils.dtypes.inner.str.add import Add


def test_end_line():
    assert Add.end_line('Hello') == 'Hello\n'
