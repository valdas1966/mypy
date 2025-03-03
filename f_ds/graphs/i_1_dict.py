from f_ds.graphs.i_0_base import GraphBase, Node
from f_core.mixins.has_uid import UID
from f_core.mixins.equable import Equable
from typing import Generic, Type, Iterable


class GraphDict(Generic[Node, UID], GraphBase[Node], Equable):
    """
    ============================================================================
     Dict-Based Graph.
    ============================================================================
    """

    def __init__(self,
                 uids: Iterable[UID],
                 type_node: Type[Node],
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        GraphBase.__init__(self, name=name)
        self._nodes: dict[UID, Node] = {uid: type_node(uid=uid)
                                        for uid
                                        in uids}

    def nodes(self) -> list[Node]:
        """
        ========================================================================
         Return a List of Graph's Nodes.
        ========================================================================
        """
        return list(self._nodes.values())

    def nodes_by_uids(self,
                      uid: UID = None,
                      uids: Iterable[UID] = None) -> Node | list[Node]:
        """
        ========================================================================
         Return a Node by a given UID.
        ========================================================================
        """
        if uid:
            return self._nodes[uid]
        elif uids:
            return [self._nodes[uid] for uid in uids]
        return list()
        
    def key_comparison(self) -> dict:
        """
        ========================================================================
         Compare by a Dict of Nodes.
        ========================================================================
        """
        return self._nodes
