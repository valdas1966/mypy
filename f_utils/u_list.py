from typing import TypeVar, Callable
import random

Item = TypeVar('Item')

"""
================================================================================
 Utils-Class for List.
================================================================================
"""


def to_filter(li: list[Item],
              predicate: Callable[[Item], bool]) -> list[Item]:
    """
    ============================================================================
     Return a Filtered-List (only Items that met Predicate-Condition).
    ============================================================================
    """
    return list(filter(predicate, li))


def to_sample(li: list[Item],
              predicate: Callable[[Item], bool] = None,
              pct: int = None,
              size: int = None
              ) -> list[Item]:
    """
    ============================================================================
     Return a Random-Sample List in a given Size or Percentage.
    ============================================================================
    """
    if predicate:
        li = to_filter(li=li, predicate=predicate)
    if pct:
        size = int(len(li) / 100 * pct)
    if not pct and not size:
        return li
    return random.sample(population=li, k=size)
