from __future__ import annotations
from f_graph.node import NodeGraph, UID
from f_core.mixins.parentable import Parentable


class NodePath(NodeGraph[UID], Parentable):
    """
    ============================================================================
     Node with Path functionality.
    ============================================================================
    """

    def __init__(self,
                 uid: UID,
                 name: str = None,
                 parent: NodePath = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeGraph.__init__(self, uid=uid, name=name)
        Parentable.__init__(self, parent=parent)
