import pytest

from f_graph.nodes.i_2_g import HasG


@pytest.fixture
def ex_a() -> HasG:
    return HasG()


@pytest.fixture
def ex_b(ex_a) -> HasG:
    return HasG(parent=ex_a)


@pytest.fixture
def ex_c(ex_b) -> HasG:
    return HasG(parent=ex_b)


def test_g(ex_a, ex_b):
    assert ex_a.g == 0
    assert ex_b.g == 1


def test_is_better_parent(ex_a, ex_b, ex_c):
    assert ex_c.is_better_parent(parent_new=ex_a)


def test_key_comparison(ex_a, ex_b):
    assert ex_b < ex_a


def test_repr(ex_a):
    assert repr(ex_a) == '<HasG: None> G=0'
