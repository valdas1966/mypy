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


def pairs(data: Iterable[Item],
          size: int,
          predicate: Callable[[Item, Item], bool] = None,
          tries: int = 100) -> list[tuple[Item, Item]]:
    """
    ============================================================================
     1. Return a list of pairs from the iterable that satisfy the predicate.
     2. If no pairs are found after {retries} -> return the list found so far.
    ============================================================================
    """
    s: set[tuple[Item, Item]] = set()
    for _ in range(tries):
        a, b = sample(data=data, size=2)
        if predicate and not predicate(a, b):
            continue
        s.add((a, b))
        if len(s) == size:
            return list(s)
    return list(s)
