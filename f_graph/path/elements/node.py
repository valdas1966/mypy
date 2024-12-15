from __future__ import annotations
from f_graph.elements.node import NodeGraph, UID
from f_graph.path.elements.mixins.has_g import HasG
from f_graph.path.elements.mixins.has_h import HasH


class NodePath(NodeGraph[UID], HasG, HasH):
    """
    ============================================================================
     NodeGraph with Path functionality.
    ============================================================================
    """

    def __init__(self,
                 uid: UID,
                 parent: NodePath = None,
                 h: int = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeGraph.__init__(self, uid=uid, name=name)
        HasG.__init__(self, parent=parent)
        HasH.__init__(self, h=h)
