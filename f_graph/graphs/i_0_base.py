from abc import abstractmethod
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.iterable import Iterable
from f_graph.nodes.i_0_base import NodeBase
from typing import TypeVar, Generic

Node = TypeVar('Node', bound=NodeBase)


class GraphBase(Generic[Node], Iterable[Node], Nameable):
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

    def to_list(self) -> list[Node]:
        """
        ========================================================================
         Return list list representation of the Object.
        ========================================================================
        """
        return self.nodes()
