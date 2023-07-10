import math


def max_permutations(values: 'sequence', k: int) -> int:
    """
    ============================================================================
     Desc: Return Max-Potential-Permutations of Sequence.
    ============================================================================
    """
    n = len(values)
    return math.perm(n, k)
