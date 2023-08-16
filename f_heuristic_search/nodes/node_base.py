from __future__ import annotations
from typing import Type, Optional


class NodeBase:
    """
    ============================================================================
     Desc: Represents a Node in with a Parent and a Weight-Value (w).
    ============================================================================
    """

    def __init__(self,
                 w: int = 0,                     # Node's Weight-Value.
                 parent: Optional[NodeBase] = None  # Parent-Node.
                                                    # None on a Start-Node.
                 ) -> None:
        """
        ========================================================================
         Desc: Init the Node object with Node's Parent and Weight value.
        ========================================================================
        """
        self._w = w
        self._parent = parent

    @property
    def w(self) -> int:
        return self._w

    @property
    def parent(self) -> Optional[NodeBase]:
        return self._parent

    @parent.setter
    def parent(self, parent_new: NodeBase) -> None:
        self._parent = parent_new
