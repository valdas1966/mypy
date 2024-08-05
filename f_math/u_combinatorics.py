from itertools import product


def cartesian_product(a: int, b: int) -> list[tuple[int, int]]:
    """
    ============================================================================
     Desc: Returns the Cartesian-Product of 2 Ranges [0,list), [0,b).
    ============================================================================
     Example:
    ----------------------------------------------------------------------------
     cartesian_product(2, 3) -> [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    ============================================================================
    """
    li_a = range(a)
    li_b = range(b)
    prod = product(li_a, li_b)
    return list(prod)
