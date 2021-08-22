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


def plus(a, b):
    """
    ============================================================================
     Description: Return Result of Addition of two given Integers.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. a : int
        2. b : int
    ============================================================================
     Return: int
    ============================================================================
    """
    if a < b:
        a, b = b, a
    i = 0
    summer = 0
    prev = 0
    while a >= 10**i:
        d_a = digit_at(a, i)
        d_b = digit_at(b, i)
        remainder, prev = u_digit.plus(d_a, d_b, prev)
        summer += remainder * (10**i)
        i += 1
    summer += prev * (10**i)
    return summer


def minus(a, b):
    assert type(a) == int
    assert type(b) == int
    assert a >= 0
    assert b >= 0



def mult_digit_int(d, n):
    """
    ============================================================================
     Description: Return Multiplication of given Digit and Integer.
                    (Sub-Function for mult(a, b))
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. d : int (Digit from 0 to 9)
        2. n : int
    ============================================================================
     Return: int
    ============================================================================
    """
    assert type(d) == int
    assert type(n) == int
    assert 0 <= d <= 9
    assert n >= 0
    i, prev, summer = 0, 0, 0
    while n >= 10**i:
        d_n = digit_at(n, i)
        remainder, prev = u_digit.mult(d, d_n, prev)
        # sum and shift
        summer += remainder * 10**i
        i += 1
    return summer + prev * 10**i


def mult(a, b):
    """
    ============================================================================
     Description: Return the Result of Multiplication of two given Integers.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. a : int
        2. b : int
    ============================================================================
     Return: int
    ============================================================================
    """
    assert type(a) == int
    assert type(b) == int
    assert a >= 0
    assert b >= 0
    i, summer = 0, 0
    while a >= 10**i:
        d = digit_at(a, i)
        # sum and shift
        summer += mult_digit_int(d, b) * (10**i)
        i += 1
    return summer


def pow(a, b):
    """
    ============================================================================
     Description: Return a^b.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. a : int
        2. b : int
    ============================================================================
     Return: int
    ============================================================================
    """
    assert type(a) == int
    assert type(b) == int
    assert a >= 0
    assert b >= 0
    ret = 1
    for _ in range(b):
        ret *= a
    return ret
