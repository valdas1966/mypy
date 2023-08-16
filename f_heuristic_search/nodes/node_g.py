from __future__ import annotations
from typing import Optional
from f_heuristic_search.nodes.node_base import NodeBase


class NodeG(NodeBase):
    """
    ============================================================================
     Represents a Node with a Cost-Value from the Start-Node (g).
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. g (int) : Cost from the Start-Node to current.
    ============================================================================
    """

    def __init__(self,
                 w: int = 0,
                 parent: NodeG = None) -> None:
        """
        ========================================================================
         Generate a new NodeG object. Computes G-Value based on Cost from the
          Start-Node to the Parent-Node + current Node's Weight.
        ========================================================================
        """
        NodeBase.__init__(w=w, parent=parent)
        self._g = self.parent.g + self._w if self.parent else 0

    @property
    def g(self) -> int:
        return self._g

    @property
    def parent(self) -> Optional[NodeG]:
        return self._parent

    @parent.setter
    def parent(self, parent_new: NodeG) -> None:
        self._parent = parent_new
        self._g = parent_new.g + self._w
