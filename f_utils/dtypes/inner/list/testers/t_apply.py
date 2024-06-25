from f_utils.dtypes.inner.list.apply import Apply


def test_except_last():
    li = ['a', 'b']
    func = lambda x: f'{x}\n'
    assert Apply.except_last(li, func) == ['a\n', 'b']