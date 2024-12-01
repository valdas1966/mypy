from __future__ import annotations
from f_graph.nodes.i_0_base import NodeBase
from f_core.mixins.parentable import Parentable


class NodePath(NodeBase, Parentable):
    """
    ============================================================================
     Node with Path functionality.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 parent: NodePath = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeBase.__init__(self, name=name)
        Parentable.__init__(self, parent=parent)
