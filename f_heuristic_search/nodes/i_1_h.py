from __future__ import annotations
from f_heuristic_search.nodes.i_0_has_cost import NodeHasCost


class NodeH(NodeHasCost):
    """
    ============================================================================
     Node with a H-Value (Heuristic cost for reaching the Goal).
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 parent: NodeH = None,
                 h: int = None) -> None:
        NodeHasCost.__init__(self, name, parent)
        self._h = h

    @property
    # Heuristic-Cost for reaching the Goal.
    def h(self) -> int:
        return self._h

    @h.setter
    def h(self, new_value: int) -> None:
        self._h = new_value

    def cost(self) -> int:
        """
        ========================================================================
         Returns Node's Cost-Func (the H-Value).
        ========================================================================
        """
        return self._h
