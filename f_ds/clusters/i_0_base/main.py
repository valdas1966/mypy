from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from f_core.mixins.has.name.main import HasName
from f_ds.mixins.collectionable.main import Collectionable, IterableSized

Item = TypeVar('Item')


class Cluster(Generic[Item], Collectionable[Item], HasName, ABC):
    """
    ============================================================================
     Cluster: a labelled set of members with an optional representative.
    ============================================================================
     Domain-agnostic abstract base. A Cluster is a named collection of
     members (the items that belong together) that may expose a single
     `representative` member (centroid / medoid / seed / center).

     Storage is abstract: a concrete subclass owns its members and
     implements `to_iterable()` — which drives `len`/`in`/`iter`/`bool`
     via the `Collectionable` mixin. The base adds only identity (`name`),
     the public `members` accessor, and the `representative` slot.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # Cluster's identity / label
                 name: str = 'Cluster') -> None:
        """
        ========================================================================
         Init the Cluster's identity (`name`). Concrete subclasses must
         initialise their own member storage.
        ========================================================================
        """
        HasName.__init__(self, name=name)

    @abstractmethod
    def to_iterable(self) -> IterableSized[Item]:
        """
        ========================================================================
         Return the underlying members (abstract — subclass owns storage).
        ========================================================================
        """
        pass

    @property
    def members(self) -> list[Item]:
        """
        ========================================================================
         Return the Cluster's members as a list (a copy of to_iterable()).
        ========================================================================
        """
        return list(self.to_iterable())

    @property
    def representative(self) -> Item | None:
        """
        ========================================================================
         Return the Cluster's representative (centroid / medoid / seed /
         center). Default None — subclasses with a distinguished member
         override.
        ========================================================================
        """
        return None

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR: 'name(size=n)'.
        ========================================================================
        """
        return f'{self.name}(size={len(self)})'

    def __repr__(self) -> str:
        """
        ========================================================================
         Return the representation of the Cluster.
        ========================================================================
        """
        return (f'<{type(self).__name__}: '
                f'name={self.name}, '
                f'size={len(self)}>')
