from f_core.components.rate_success import RateSuccess


def test_empty():
    r = RateSuccess()
    assert str(r) == '[0/0]'


def test_update():
    r = RateSuccess()
    r.update(is_success=True)
    r.update(is_success=False)
    assert r.rate() == 0.5
    assert str(r) == '[1/2]'
