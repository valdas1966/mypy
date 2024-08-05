from f_utils.dtypes.inner.a.apply import Apply


def test_except_last():
    li = ['list', 'b']
    func = lambda x: f'{x}\n'
    assert Apply.except_last(li, func) == ['list\n', 'b']
