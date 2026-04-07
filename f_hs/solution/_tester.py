import pytest
from f_hs.solution import SolutionSPP


@pytest.fixture
def valid() -> SolutionSPP:
    """
    ========================================================================
     Create a valid SolutionSPP.
    ========================================================================
    """
    return SolutionSPP.Factory.valid()


@pytest.fixture
def invalid() -> SolutionSPP:
    """
    ========================================================================
     Create an invalid SolutionSPP.
    ========================================================================
    """
    return SolutionSPP.Factory.invalid()


@pytest.fixture
def zero() -> SolutionSPP:
    """
    ========================================================================
     Create a zero-cost SolutionSPP.
    ========================================================================
    """
    return SolutionSPP.Factory.zero()


def test_valid(valid: SolutionSPP) -> None:
    """
    ========================================================================
     Test that a valid solution is truthy.
    ========================================================================
    """
    assert bool(valid) is True


def test_invalid(invalid: SolutionSPP) -> None:
    """
    ========================================================================
     Test that an invalid solution is falsy.
    ========================================================================
    """
    assert bool(invalid) is False


def test_cost(valid: SolutionSPP) -> None:
    """
    ========================================================================
     Test the cost property.
    ========================================================================
    """
    assert valid.cost == 5.0


def test_zero_cost(zero: SolutionSPP) -> None:
    """
    ========================================================================
     Test that zero cost is valid.
    ========================================================================
    """
    assert bool(zero) is True
    assert zero.cost == 0.0
