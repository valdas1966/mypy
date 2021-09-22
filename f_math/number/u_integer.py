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
    assert b >= 1
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
    assert b >= 1
    return a - b * (div(a, b))


def length(n):
    """
    ============================================================================
     Description: Return the number of digits in the given Integer.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. n : int
    ============================================================================
     Return: int (Number of Digits in the given Integer).
    ============================================================================
    """
    assert type(n) == int
    assert n >= 0
    return len(str(n))


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


def digits(n):
    """
    ============================================================================
     Description: Return List of Integer's Digits ordered from right to left.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. n : int
    ============================================================================
     Return: list of int (List of Digits).
    ============================================================================
    """
    assert type(n) == int
    assert n >= 0
    if not n:
        return [0]
    i = 0
    li = list()
    while n >= 10**i:
        d = digit_at(n, i)
        li.append(d)
        i += 1
    return li


def shift_left(n, i):
    """
    ============================================================================
     Description: Shift Integer i places Left.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. n : int (int to shift)
        2. i : int (places to shift)
    ============================================================================
     Return: int (Shifted Integer)
    ============================================================================
    """
    assert type(n) == int
    assert type(i) == int
    assert n >= 0
    assert i >= 0
    # shift i places left
    return n * 10**i


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
    assert type(a) == int
    assert type(b) == int
    assert a >= 0
    assert b >= 0
    a, b = max(a, b), min(a, b)
    res, d_prev = 0, 0
    for i, d_a in enumerate(digits(a)):
        d_b = digit_at(b, i)
        d_remainder, d_prev = u_digit.plus(d_a, d_b, d_prev)
        res += shift_left(d_remainder, i)
    res += shift_left(d_prev, length(a))
    return res


def minus(a, b):
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
    assert type(a) == int
    assert type(b) == int
    assert a >= 0
    assert b >= 0
    if a < b:
        return -minus(b, a)
    d_prev, res = 0, 0
    for i, d_a in enumerate(digits(a)):
        d_b = digit_at(b, i)
        d_remainder, d_prev = u_digit.minus(d_a, d_b, d_prev)
        res += shift_left(d_remainder, i)
    return res


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
    d_prev, res = 0, 0
    for i, d_n in enumerate(digits(n)):
        d_remainder, d_prev = u_digit.mult(d, d_n, d_prev)
        res += shift_left(d_remainder, i)
    res += shift_left(d_prev, length(n))
    return res


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
    res = 0
    for i, d in enumerate(digits(a)):
        res += shift_left(mult_digit_int(d, b), i)
    return res


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
    res = 1
    for _ in range(b):
        res *= a
    return res
