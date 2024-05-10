from abc import ABC, abstractmethod
from f_abstract.mixins.nameable import Nameable
from f_ds.nodes.i_0_base import NodeBase
from typing import TypeVar, Generic

Node = TypeVar('Node', bound=NodeBase)


class GraphBase(ABC, Generic[Node], Nameable):
    """
    ============================================================================
     Base Graph.
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name)

    @abstractmethod
    def get_neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Returns a List of a given Node's neighbors.
        ========================================================================
        """
        pass
