from typing import Generic, TypeVar, Iterator

T = TypeVar('T')   # Type for Elements in the Set


class SetOrdered(Generic[T], dict):
    """
    ============================================================================
     Set of Elements sorted by their Insertion-Order.
    ============================================================================
    """

    def __init__(self):
        """
        ========================================================================
         Init an empty Dict.
        ========================================================================
        """
        super().__init__()

    def add(self, element: T) -> None:
        """
        ========================================================================
         Add list new Element to the Set.
        ========================================================================
        """
        self[element] = None

    def remove(self, element: T) -> None:
        """
        ========================================================================
         Remove an Element from the Set.
        ========================================================================
        """
        super().pop(element)

    def __str__(self) -> str:
        """
        ========================================================================
         1. Return as STR-REPR of the Set.
         2. Example: 'SetOrdered([1, 2])'
        ========================================================================
        """
        elements = list(self)
        return f'{self.__class__.__name__}({elements})'

    def __repr__(self) -> str:
        return self.__str__()
