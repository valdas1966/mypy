from typing import TypeVar, Generic
from f_abstract.mixins.nameable_sortable import NameableAndSortable
T = TypeVar('T', bound=NameableAndSortable)


class Open(Generic[T]):
    """
    ============================================================================
     Data Structure for Nameable and Sortable objects.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. pop() -> T
           [*] Pops the minimal Item O(n).
        2. push(item: T) -> None
           [*] Inserts a new Item to the Structure O(1).
        3. get(name: str) -> T
           [*] Returns Item by Name O(1).
        4. items() -> list[T]
           [*] Returns a list of all items
    ============================================================================
     Magic Methods:
    ----------------------------------------------------------------------------
        1. len -> int
        2. contains(item T) -> bool
    ============================================================================
    """

    _d: dict[str: T]

    def __init__(self) -> None:
        """
        ========================================================================
         Initializes the private Dictionary.
        ========================================================================
        """
        self._d = dict()

    def pop(self) -> T:
        """
        ========================================================================
         Pops the Minimal Item.
        ========================================================================
        """
        val_min = min(self._d.values())
        key_min = min(self._d, key=self._d.get)
        del self._d[key_min]
        return val_min

    def push(self, item: T) -> None:
        """
        ========================================================================
         Pushes new Node into the Structure.
        ========================================================================
        """
        self._d[item.name] = item

    def get(self, item: T) -> T:
        """
        ========================================================================
         Returns the Node by its Name.
        ========================================================================
        """
        return self._d[item.name]

    def items(self) -> list[T]:
        """
        ========================================================================
         Returns a list of all items.
        ========================================================================
        """
        return list(self._d.values())

    def __len__(self) -> int:
        """
        ========================================================================
         Returns number of Items in the Structure.
        ========================================================================
        """
        return len(self._d)

    def __contains__(self, item: T) -> bool:
        """
        ========================================================================
         Returns True if a Structure contains the given Item.
        ========================================================================
        """
        return item.name in self._d
