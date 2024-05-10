from __future__ import annotations
from f_ds.nodes.i_1_path import NodePath


class NodeH(NodePath):
    """
    ============================================================================
     Node with a H-Value (Heuristic cost for reaching the Goal).
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 parent: NodeH = None) -> None:
        NodePath.__init__(self, name=name, parent=parent)
        self._h = None

    @property
    # Heuristic-Cost for reaching the Goal.
    def h(self) -> int:
        return self._h

    @h.setter
    def h(self, new_value: int) -> None:
        self._h = new_value

    def key_comparison(self) -> list[int]:
        """
        ========================================================================
         Returns Node's Cost-Func (the H-Value).
        ========================================================================
        """
        return [self._h]
