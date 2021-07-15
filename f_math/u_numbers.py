
def factors(n):
    """
    ============================================================================
     Description: Return sorted List of Factors of the given Integer.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. n : int
    ============================================================================
     Return: list of int (Sorted List of Factors).
    ============================================================================
    """
    assert type(n) == int
    s = {1, n}
    for i in range(2, n//2+1):
        if i in s:
            break
        if n % i == 0:
            s.update({i, n//i})
            if i == n//i:
                break
    return sorted([x for x in s])


def common_factors(a, b):
    """
    ============================================================================
     Description: Return sorted List of Common Factors of 2 given Integers.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. a : int
        2. b : int
    ============================================================================
     Return: list of int (Sorted List of Common Factors).
    ============================================================================
    """
    factors_a = set(factors(a))
    factors_b = set(factors(b))
    common = factors_a.intersection(factors_b)
    return sorted([x for x in common])


def gcf(a, b):
    """
    ============================================================================
     Description: Return the Greatest Common Factor of two given integers.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. a : int
        2. b : int
    ============================================================================
     Return: int (GCF of two given Integers).
    ============================================================================
    """
    common = common_factors(a, b)
    return max(common)
