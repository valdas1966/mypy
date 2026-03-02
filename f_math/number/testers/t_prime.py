import pytest
from f_math.number.u_prime import is_prime, count_primes


@pytest.mark.parametrize('n', [2, 3, 5, 7, 13, 97])
def test_is_prime_true(n: int) -> None:
    """
    ============================================================================
     Test that known primes return True.
    ============================================================================
    """
    assert is_prime(n)


@pytest.mark.parametrize('n', [0, 1, 4, 9, 100])
def test_is_prime_false(n: int) -> None:
    """
    ============================================================================
     Test that non-primes return False.
    ============================================================================
    """
    assert not is_prime(n)


def test_count_primes() -> None:
    """
    ============================================================================
     Test count_primes on [1..10] — primes are 2, 3, 5, 7.
    ============================================================================
    """
    assert count_primes(list(range(1, 11))) == 4
