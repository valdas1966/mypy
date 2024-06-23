import pytest
from f_abstract.mixins.nameable import Nameable


@pytest.fixture
def ex_none():
    return Nameable()

@pytest.fixture
def ex_test():
    return Nameable(name='Test')


def test_init_default(ex_none, ex_test):
    assert ex_none.name is None
    assert ex_test.name == 'Test'

def test_eq(ex_none, ex_test):
    assert ex_none == ex_none
    assert ex_none != ex_test

def test_sort(ex_none, ex_test):
    assert ex_none < ex_test

def test_str(ex_none, ex_test):
    assert str(ex_none) == 'None'
    assert str(ex_test) == 'Test'

def test_repr(ex_none, ex_test):
    assert repr(ex_none) == '<Nameable: None>'
    assert repr(ex_test) == '<Nameable: Test>'

def test_hash(ex_none, ex_test):
    assert {ex_none, ex_test, ex_test} == {ex_none, ex_test}
