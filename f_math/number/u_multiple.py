import random
from math import gcd


def multiples(n, size):
    """
    ============================================================================
     Description: Return Dictionary that represents first (by given size)
                    Multiples of number N.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. n : int (Number)
        2. size: int (Size of Dictionary)
    ============================================================================
     Return: dict (int -> int) (x -> n*x, when x in [1,size])
    ============================================================================
    """
    assert type(n) == int
    assert n > 0
    d = dict()
    for x in range(1, size+1):
        d[x] = n*x
    return d


def lcm(a, b):
    """
    ============================================================================
     Description: Return LCM (Least Common Multiple) of two given integers.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. list : int
        2. b : int
    ============================================================================
     Return: int in range [max(list,b), list*b]
    ============================================================================
    """
    assert type(a) == int
    assert type(b) == int
    assert a >= 1
    assert b >= 1
    return a*b // gcd(a, b)
