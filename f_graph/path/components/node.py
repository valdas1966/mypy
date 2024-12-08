from __future__ import annotations
from f_graph.node import NodeGraph, UID
from f_ds.mixins.has_parent import HasParent


class NodePath(NodeGraph[UID], HasParent):
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
        HasParent.__init__(self, parent=parent)
