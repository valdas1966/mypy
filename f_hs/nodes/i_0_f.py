from __future__ import annotations
from f_ds.graphs.nodes.i_1_cell import NodeCell, Cell


class NodeF(NodeCell):
    """
    ============================================================================
     Node represents a Cell in the Grid with an associated F-Cost function.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 cell: Cell = Cell(),
                 parent: NodeF = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(name=name, cell=cell, parent=parent)
        self._g = (parent.g + 1) if parent else 0
        self._h = None

    @property
    def g(self) -> int:
        """
        ========================================================================
         Cost from Start to current Node.
        ========================================================================
        """
        return self._g

    @property
    def h(self) -> int:
        """
        ========================================================================
         Heuristic cost from current Node to Goal.
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

    @NodeCell.parent.setter
    def parent(self, p: NodeF) -> None:
        """
        ========================================================================
         Set a new Parent and update the G-Value respectively.
        ========================================================================
        """
        self._parent = p
        self._g = p.g + 1

    def f(self) -> int:
        """
        ========================================================================
         Calculate the total Estimated Cost (G + H).
        ========================================================================
        """
        return (self._g + self._h) if self._h is not None else None

    def is_better_parent(self, parent: NodeF) -> bool:
        """
        ========================================================================
         Check if the new parent is better than the current based on G-Value.
        ========================================================================
        """
        return self._parent is None or (parent.g < self.parent.g)

    def key_comparison(self) -> list:
        """
        ========================================================================
         If F-Values are equal, break ties on H-Value.
        ========================================================================
        """
        return [self.f(), self.h, NodeCell.key_comparison(self)]

    def __repr__(self) -> str:
        """
        ========================================================================
         '<NodeF: Name(Row,Col)> G=5, H=10, F=15'
        ========================================================================
        """
        prefix = NodeCell.__repr__(self)
        return f'{prefix} G={self._g}, H={self._h}, F={self.f}'
