from __future__ import annotations
from f_hs.nodes.i_0_g import NodeG
from f_hs.nodes.i_0_h import NodeH


class NodeF(NodeG, NodeH):
    """
    ============================================================================
     Informed Node with F-Value (G + H).
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 parent: NodeF = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(name=name, parent=parent)

    def f(self) -> int:
        """
        ========================================================================
         Calculate the total Estimated Cost (G + H).
        ========================================================================
        """
        return (self._g + self._h) if self._h is not None else None

    def key_comparison(self) -> list:
        """
        ========================================================================
         If F-Values are equal, break ties on H-Value.
        ========================================================================
        """
        return [self.f(), NodeG.key_comparison(self)]

    def __repr__(self) -> str:
        """
        ========================================================================
         '<NodeF: Name> G=5, H=10, F=15'
        ========================================================================
        """
        return f'{NodeG.__repr__(self)}, H={self.h}, F={self.f()}'
