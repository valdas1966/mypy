from f_abstract.mixins.nameable import Nameable
from typing import TypeVar, Generic
T = TypeVar('T', bound=Nameable)


class Closed(Generic[T]):
    """
    ============================================================================
     Data Structure for Nameable objects.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. push(item: T) -> None
           [*] Pushes a new Item into the Structure.
        2. get(item: T) -> T
           [*] Returns an Item from the Structure by its name.
        3. items() -> list[T]
           [*] Returns Structure's Items in Insertion-Order.
    ============================================================================
     Magic Methods:
    ----------------------------------------------------------------------------
        1. contains -> bool
    ============================================================================
    """

    def __init__(self):
        """
        ========================================================================
         Inits the private Dictionary.
        ========================================================================
        """
        self._d = dict()

    def push(self, item: T) -> None:
        """
        ========================================================================
         Push a new Item into a Structure.
        ========================================================================
        """
        self._d[item.name] = item

    def get(self, item: T) -> T:
        """
        ========================================================================
         Returns an Item from the Structure by its Name.
        ========================================================================
        """
        return self._d[item.name]

    def items(self) -> list[T]:
        """
        ========================================================================
         Returns a list of all Items in the Structure in Insertion-Order.
        ========================================================================
        """
        return list(self._d.values())

    def __contains__(self, item: T) -> bool:
        """
        ========================================================================
         Returns True if the given Item is in the Structure.
        ========================================================================
        """
        return item.name in self._d
