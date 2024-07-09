from __future__ import annotations
from f_ds.graphs.nodes.i_0_base import NodeBase
from f_abstract.mixins.parentable import Parentable


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
