from typing import Iterable, TypeVar, Callable
import random


Key = TypeVar('Key')
Item = TypeVar('Item')
Pair = tuple[Item, Item]


def sample(items: Iterable[Item],
           size: int = None,
           pct: int = None,
           predicate: Callable[[Item], bool] = None) -> list[Item]:
    """
    ============================================================================
     Return a random sample of the iterable.
    ============================================================================
    """
    if not isinstance(items, list):
        items = list(items)
    if not size:
        size = int(len(items) * pct / 100)
    if predicate:
        items = [item for item in items if predicate(item)]
    return random.sample(population=items, k=size)


def filter(items: Iterable[Item],
           predicate: Callable[[Item], bool]) -> list[Item]:
    """
    ============================================================================
     Return a list of items that satisfy the predicate.
    ============================================================================
    """
    return [item for item in items if predicate(item)]


def pairs(items: Iterable[Item],
          size: int,
          predicate: Callable[[Item, Item], bool] = None,
          blacklist: Iterable[Pair] = None,
          tries: int = None) -> list[Pair]:
    """
    ============================================================================
     1. Return a list of pairs from the iterable that satisfy the predicate.
     2. The pairs are unique and ordered.
     3. The pairs are not in the blacklist.
     4. If not enough pairs are found after {tries}
             -> return the list found so far.
    ============================================================================
    """
    if not tries:
        tries = size * 100
    s: set[Pair] = set()
    for _ in range(tries):
        a, b = sample(items=items, size=2)
        if predicate and not predicate(a, b):
            continue
        if blacklist and (a, b) in blacklist:
            continue
        s.add((a, b))
        if len(s) == size:
            return list(s)
    return list(s)


def distribute(items: Iterable[Item],
               keys: Iterable[Key]) -> dict[Key, list[Item]]:
    """
    ============================================================================
     Distribute the data into keys.
    ----------------------------------------------------------------------------
     Example:
    ----------------------------------------------------------------------------
     >>> items = [1, 2, 3, 4]
     >>> keys = ['a', 'b']
     >>> distribute(items, keys)
     {'a': [1, 2], 'b': [3, 4]}
    ============================================================================
    """
    if not isinstance(items, list):
        items = list(items)
    if not isinstance(keys, list):
        keys = list(keys)
    # Size of each chunk
    size = len(items) // len(keys)
    # Dictionary to store the distributed data
    out: dict[Key, list[Item]] = dict()
    # Distribute by chunk slices
    for i, key in enumerate(keys):
        # Start and finish indices of the chunk
        start: int = i * size
        finish: int = start + size
        # Data of the chunk
        chunk: list[Item] = items[start:finish]
        # Add the chunk to the dictionary
        out[key] = chunk
    # Return the dictionary
    return out
