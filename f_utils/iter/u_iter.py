from typing import Iterable, TypeVar, Callable
import random

Item = TypeVar('Item')


def sample(data: Iterable[Item],
           size: int = None,
           pct: int = None) -> list[Item]:
    """
    ============================================================================
     Return a random sample of the iterable.
    ============================================================================
    """
    data = list(data)
    if not size:
        size = int(len(data) * pct / 100)
    return random.sample(population=data, k=size)


def filter(data: Iterable[Item],
           predicate: Callable[[Item], bool]) -> list[Item]:
    """
    ============================================================================
     Return a list of items that satisfy the predicate.
    ============================================================================
    """
    return [item for item in data if predicate(item)]
