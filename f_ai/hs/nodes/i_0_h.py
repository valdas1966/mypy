from __future__ import annotations
from f_graph.path.ds._old_node import NodePath


class NodeH(NodePath):
    """
    ============================================================================
     Node with H-Value (Heuristic Cost from current Node to Goal).
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodePath.__init__(self, name=name)
        self._h = None

    @property
    def h(self) -> int:
        """
        ========================================================================
         Heuristic Cost from current Node to Goal.
        ========================================================================
        """
        return self._h

    @h.setter
    def h(self, val: int) -> None:
        """
        ========================================================================
         Set Heuristic Cost from current Node to Goal.
        ========================================================================
        """
        self._h = val

    def key_comparison(self) -> list:
        """
        ========================================================================
         Prefer Nodes with lower H-Value (less uncertainty).
        ========================================================================
        """
        return [self.h]

    def __repr__(self) -> str:
        """
        ========================================================================
         Ex: '<NodeH: A> H=1'
        ========================================================================
        """
        return f'{NodePath.__repr__(self)} H={self.h}'
