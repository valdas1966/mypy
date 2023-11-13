from __future__ import annotations
from f_heuristic_search.nodes.i_1_g import NodeG
from f_heuristic_search.nodes.i_1_h import NodeH


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
                 parent: NodeF = None) -> None:
        NodeG.__init__(self, name, parent)
        NodeH.__init__(self, name, parent)

    def f(self) -> int:
        """
        ========================================================================
         1. Estimates the cost of the optimal path from the start node to the
             goal node through this Node.
         2. This estimate is used to prioritize nodes during the search.
        ========================================================================
        """
        return self.g + self.h

    def cost(self) -> list[int]:
        """
        ========================================================================
         Returns Node's Cost-Func (F-Value, and G-Value on Tie-Break).
        ========================================================================
        """
        return [self.f(), NodeG.cost(self)]
