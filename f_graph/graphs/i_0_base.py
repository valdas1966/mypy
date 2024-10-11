from abc import abstractmethod
from typing import TypeVar, Generic
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.groupable import Groupable, Group
from f_graph.nodes.i_0_base import NodeBase


Node = TypeVar('Node', bound=NodeBase)


class GraphBase(Generic[Node], Groupable[Node], Nameable):
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
    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Returns list List of list given Node's neighbors.
        ========================================================================
        """
        pass

    def to_group(self, name: str = None) -> Group[Node]:
        """
        ========================================================================
         Return list list representation of the Object.
        ========================================================================
        """
        return Group(name=name, data=self.nodes())
