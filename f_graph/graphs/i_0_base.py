from abc import abstractmethod
from typing import TypeVar, Generic
from f_core.mixins.nameable import Nameable
from f_core.abstracts.copyable import Copyable
from f_ds.mixins.groupable import Groupable, Group
from f_graph.nodes.i_0_base import NodeBase

Node = TypeVar('Node', bound=NodeBase)


class GraphBase(Generic[Node], Groupable[Node], Nameable, Copyable):
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

    def children(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return List of Node's Neighbors that are not parents of the Node.
        ========================================================================
        """
        return [child
                for child
                in self.neighbors(node=node)
                if child.parent != node]

    def to_group(self, name: str = None) -> Group[Node]:
        """
        ========================================================================
         Return list list representation of the Object.
        ========================================================================
        """
        return Group(name=name, data=self.nodes())
