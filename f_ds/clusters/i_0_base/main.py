from __future__ import annotations
from f_ds.mixins.collectionable import Collectionable, IterableSized
from f_core.mixins import HasName
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Item = TypeVar('Item')


class ClusterBase(Generic[Item], Collectionable[Item], HasName, ABC):
    """
    ============================================================================
     ClusterBase: a labeled set of members with an optional representative.
    ============================================================================
     Domain-agnostic abstract base. A Cluster is a named collection of
     members (the items that belong together) that may expose a single
     `representative` member (centroid / medoid / seed / center).

     Storage is abstract: a concrete subclass owns its members and
     implements `to_iterable()` — which drives `len`/`in`/`iter`/`bool`
     via the `Collectionable` mixin. The base adds only identity (`name`),
     the public `members` accessor, and the `representative` slot.

     Concrete subclasses: `ClusterList` (explicit members, this package);
     the grid clusters in `f_ds/grids/cluster/` (`ClusterDiamond`, …).
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
         initialize their own member storage.
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
         Return STR-REPR: 'name(size=n)', plus 'rep=…' when the Cluster
         has a representative. (__repr__ comes from HasRepr → wraps this.)
        ========================================================================
        """
        rep = self.representative
        if rep is None:
            return f'{self.name}(size={len(self)})'
        return f'{self.name}(size={len(self)}, rep={rep})'
