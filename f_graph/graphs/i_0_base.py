from abc import abstractmethod
from typing import TypeVar, Generic
from f_core.mixins.nameable import Nameable
from f_core.abstracts.clonable import Clonable
from f_ds.mixins.groupable import Groupable, Group
from f_graph.node import NodeGraph

Node = TypeVar('Node', bound=NodeGraph)


class GraphBase(Generic[Node], Groupable[Node], Nameable, Clonable):
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
