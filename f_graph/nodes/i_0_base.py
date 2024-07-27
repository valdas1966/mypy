from __future__ import annotations
from f_abstract.mixins.nameable import Nameable


class NodeBase(Nameable):
    """
    ============================================================================
     Node Base-Class.
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
