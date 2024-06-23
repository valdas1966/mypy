from abc import ABC, abstractmethod
from f_abstract.mixins.nameable import Nameable
from f_ds.graphs.nodes.i_0_base import NodeBase
from typing import TypeVar, Generic

Node = TypeVar('Node', bound=NodeBase)


class GraphBase(ABC, Generic[Node], Nameable):
    """
    ============================================================================
     Graph Base-Class.
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
    def nodes(self) -> list[Node]:
        """
        ========================================================================
         Return List of Nodes in the Graph.
        ========================================================================
        """
        pass

    @abstractmethod
    def get_neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Returns a List of a given Node's neighbors.
        ========================================================================
        """
        pass

    def __len__(self) -> int:
        """
        ========================================================================
         Return the number of Nodes in the Grid.
        ========================================================================
        """
        return len(self.nodes())

    def __bool__(self) -> bool:
        """
        ========================================================================
         Return True if the Graph is not Empty.
        ========================================================================
        """
        return bool(len(self))
