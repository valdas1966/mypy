from f_utils.dtypes.u_int import UInt as u_int


def test_to_str():
    assert u_int.to_str(num=1_000_000) == '1.0M'
    assert u_int.to_str(num=1_000) == '1.0K'
    assert u_int.to_str(num=100) == '100'


def test_pct():
    assert u_int.pct(part=7, total=10) == 70


def test_part():
    assert u_int.part(total=10, pct=70) == 7
