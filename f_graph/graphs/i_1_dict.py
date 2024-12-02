from f_graph.graphs.i_0_base import GraphBase, Node
from f_core.mixins.has_uid import HasUID, UID
from typing import Generic, Type, Iterable


class GraphDict(Generic[Node, UID], GraphBase[Node], HasUID[UID]):
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

    def node_from_uid(self, uid: UID) -> Node:
        """
        ========================================================================
         Return a Node by a given UID.
        ========================================================================
        """
        return self._nodes[uid]
