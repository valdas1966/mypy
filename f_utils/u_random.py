import random
from typing import Sequence
from f_utils import u_math


def to_groups(values: Sequence,
              n: int,
              k: int) -> set:
    """
    ============================================================================
     Desc: Return Set of [n] Random-Groups with [k] size.
    ============================================================================
    """
    values = list(set(values))
    if n > u_math.max_permutations(values, k):
        raise ValueError(f'n > u_math.max_permutations(values, k), '
                         f'{n} > {u_math.max_permutations(values, k)}')
    groups = set()
    while len(groups) < n:
        group = random.sample(population=values, k=k)
        group = tuple(group)
        groups.add(group)
    return groups


def sample(li: list, size: int) -> list:
    size = min(size, len(li))

