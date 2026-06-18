from __future__ import annotations
from f_ds.clusters.i_0_base.main import ClusterBase
from typing import Iterable, TypeVar

Item = TypeVar('Item')


class ClusterList(ClusterBase[Item]):
    """
    ============================================================================
     ClusterList: a Cluster built from an explicit iterable of members.
    ============================================================================
     The default concrete Cluster. Members are supplied directly (stored
     as a list — order preserved, any `Item` type, no hashability needed)
     and the representative, if any, is passed in (it need NOT be a member,
     which lets a computed point — e.g. a centroid — serve as it).

     For computed-membership clusters (BFS shapes, etc.) subclass
     `ClusterBase` directly instead — see `f_ds/grids/cluster/`.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # The Cluster's members (stored as a list; order kept)
                 members: Iterable[Item],
                 # Cluster's identity / label
                 name: str = 'ClusterList',
                 # Optional distinguished member (may be outside `members`)
                 representative: Item | None = None) -> None:
        """
        ========================================================================
         Store the explicit members and the optional representative; init
         identity (`name`) via the base.
        ========================================================================
        """
        ClusterBase.__init__(self, name=name)
        self._members: list[Item] = list(members)
        self._representative: Item | None = representative

    def to_iterable(self) -> list[Item]:
        """
        ========================================================================
         Return the underlying member list. Drives `len`/`in`/`iter`/`bool`
         via the Collectionable mixin.
        ========================================================================
        """
        return self._members

    @property
    def representative(self) -> Item | None:
        """
        ========================================================================
         Return the representative supplied at construction (default None).
        ========================================================================
        """
        return self._representative
