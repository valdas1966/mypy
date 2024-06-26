from __future__ import annotations
from f_hs.nodes.i_1_g import NodeG
from f_hs.nodes.i_1_h import NodeH


class NodeF(NodeG, NodeH):
    """
    ============================================================================
     1. Informed-Node representing its estimated location on the path between
         the Start and Goal nodes.
     2. While comparing two nodes, if they have the same f-value, the node with
         the higher g-value is considered 'lesser'. This is because the g-value
         provides a more reliable indication of path cost.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 parent: NodeF = None,
                 w: int = 1) -> None:
        NodeG.__init__(self, name=name, parent=parent, w=w)
        NodeH.__init__(self, name=name, parent=parent)

    def f(self) -> int:
        """
        ========================================================================
         1. Estimates the cost of the optimal path from the start node to the
             goal node through this Node.
         2. This estimate is used to prioritize nodes during the search.
        ========================================================================
        """
        if self.g is not None and self.h is not None:
            return self.g + self.h
        return None

    def key_comparison(self) -> list[int]:
        """
        ========================================================================
         Returns Node's Cost-Func (F-Value, and G-Value on Tie-Break).
        ========================================================================
        """
        return [self.f(), NodeG.key_comparison(self), ]
