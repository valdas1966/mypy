from f_utils import u_float


def test_are_float():
    values = [0, 1]
    assert u_float.are_float(values)
    values = [0, 1, 1.5]
    assert u_float.are_float(values)
    values = ['1', '1.5']
    assert u_float.are_float(values)
    values = ['1.5', True]
    assert u_float.are_float(values)
    values = ['1.5', 'True']
    assert not u_float.are_float(values)


def test_to_str_pct():
    assert u_float.to_str_pct(val=0.75, precision=0) == '75%'
    assert u_float.to_str_pct(val=0.75, precision=0, to_100=False) == '1%'
    assert u_float.to_str_pct(val=0.75, precision=1) == '75.0%'
    assert u_float.to_str_pct(val=0.75, precision=1, to_100=False) == '0.8%'
    assert u_float.to_str_pct(val=0.75, precision=2) == '75.00%'
    assert u_float.to_str_pct(val=0.75, precision=2, to_100=False) == '0.75%'
    assert u_float.to_str_pct(val=0.00075, precision=2) == '0.07%'
    assert u_float.to_str_pct(val=1.25, precision=2) == '125.00%'
    assert u_float.to_str_pct(val=-0.25, precision=2) == '-25.00%'
    assert u_float.to_str_pct(val=0, precision=2) == '0.00%'
    assert u_float.to_str_pct(val=1, precision=0) == '100%'
