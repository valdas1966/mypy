from f_math.number import u_digit
from random import randint


def random(value_min, value_max, count=1):
    """
    ============================================================================
     Description: Return Random Integer Numbers (from min to max inclusive).
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. value_min : int
        2. value_max : int
        3. count : int (Count of Random Numbers to Return)
    ============================================================================
     Return: tuple of int
    ============================================================================
    """
    return (randint(value_min, value_max) for _ in range(count))


def div(a, b):
    """
    ============================================================================
     Description: Return Div(a,b). Example: div(123, 10) = 12
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. a : int
        2. b : int
    ============================================================================
     Return: int (Div(a,b))
    ============================================================================
    """
    assert type(a) == int
    assert type(b) == int
    assert a >= 0
    assert b > 0
    if a < b:
        return 0
    count = 0
    while a >= b:
        a -= b
        count += 1
    return count


def mod(a, b):
    """
    ============================================================================
     Description: Return Modulo(a,b). Example: mod(123, 10) = 3
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. a : int
        2. b : int
    ============================================================================
     Return: int (Modulo(a,b))
    ============================================================================
    """
    assert type(a) == int
    assert type(b) == int
    assert a >= 0
    assert b > 0
    return a - b * (div(a, b))


def digit_at(n, i):
    """
    ============================================================================
     Description: Return Digit of given Number at the Index i.
                    i=0: the first digit from right
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. n : int (Number to extract digit from).
        2. i : int (Index of digit to extract).
    ============================================================================
     Return: int (Digit of Number n at the Index i)
    ============================================================================
    """
    assert type(n) == int
    assert type(i) == int
    assert n >= 0
    assert i >= 0
    pow_mod = 10 ** (i+1)
    pow_div = 10 ** (i)
    return (n % pow_mod) // pow_div

