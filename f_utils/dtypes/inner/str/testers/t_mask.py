import pytest
from f_utils.dtypes.inner.str.mask import Mask


@pytest.fixture
def ex_single() -> str:
    return 'abc'

@pytest.fixture
def ex_multi() -> str:
    return 'ab c'

@pytest.fixture
def ex_exception() -> str:
    return '"abc"'


def test_full(ex_single, ex_multi, ex_exception):
    assert Mask.full(ex_single) == '***'
    assert Mask.full(ex_multi) == '** *'
    assert Mask.full(ex_exception) == '"***"'


def test_pct(ex_exception):
    assert Mask.pct(s=ex_exception, pct_mask=100) == '"***"'


def test_one_word(ex_single, ex_multi):
    assert Mask.one_word(text=ex_single) == ('***', 'abc')
    assert Mask.one_word(text=ex_multi) in (('** c', 'ab'), ('ab *', 'c'))
