from abc import ABC
from f_abstract.mixins.nameable import Nameable


class NodeBase(ABC, Nameable):
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