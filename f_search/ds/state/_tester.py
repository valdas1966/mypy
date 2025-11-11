from f_search.ds.state._factory import State, Cell
import pytest


@pytest.fixture
def zero() -> State[Cell]:
    """
    ========================================================================
     Fixture for the zero State.
    ========================================================================
    """
    return State.Factory.zero()


@pytest.fixture
def one() -> State[Cell]:
    """
    ========================================================================
     Fixture for the one State.
    ========================================================================
    """
    return State.Factory.one()


def test_eq(zero: State[Cell],
            one: State[Cell]) -> None:
    """
    ========================================================================
     Test the eq() method.
    ========================================================================
    """
    assert zero == zero
    assert zero != one


def test_hash(zero: State[Cell],
              one: State[Cell]) -> None:
    """
    ========================================================================
     Test the hash() method.
    ========================================================================
    """
    assert hash(zero) == hash(zero)
    assert hash(zero) != hash(one)
    