from f_core.mixins import Comparable, Hashable
from f_core.mixins.has import HasRepr
from typing import Any, Iterator
from abc import abstractmethod


class Tupleable(Comparable, Hashable, HasRepr):
    """
    ============================================================================
     Mixin for value-record objects defined entirely by their tuple.
    ============================================================================
     Subclasses implement a single abstract `to_tuple()`; equality, ordering,
     hashing, iteration and indexing all derive from it. The tuple IS the
     identity, so a Tupleable must be IMMUTABLE — mutating it would change its
     hash and corrupt any set / dict holding it.
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    @abstractmethod
    def to_tuple(self) -> tuple:
        """
        ========================================================================
         Return the object's data as a tuple. Abstract — every subclass
         implements it; everything else here derives from it.
        ========================================================================
        """
        raise NotImplementedError

    @property
    def key(self) -> tuple:
        """
        ========================================================================
         Identity = the tuple. Drives __eq__ / __lt__ / __hash__.
        ========================================================================
        """
        return self.to_tuple()

    def __iter__(self) -> Iterator[Any]:
        """
        ========================================================================
         Iterate the tuple — enables unpacking (`a, b = obj`).
        ========================================================================
        """
        return iter(self.to_tuple())

    def __getitem__(self, index: int) -> Any:
        """
        ========================================================================
         Index into the tuple (`obj[0]`).
        ========================================================================
        """
        return self.to_tuple()[index]

    def __len__(self) -> int:
        """
        ========================================================================
         Return the number of items in the tuple.
        ========================================================================
        """
        return len(self.to_tuple())

    def __str__(self) -> str:
        """
        ========================================================================
         Return the tuple as a string. Ex: '(1, 2)'
        ========================================================================
        """
        return str(self.to_tuple())
