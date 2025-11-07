from f_graph.graphs._base import GraphBase, NodeKey
from f_core.mixins.dictable.main import Dictable
from typing import Generic, TypeVar, Self

Key = TypeVar('Key')
Node = TypeVar('Node', bound=NodeKey)


class GraphDict(Generic[Key, Node],
                GraphBase[Node],
                Dictable[Key, Node]):
    """
    ============================================================================
     Dict-Based Graph.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 data: dict[Key, Node],
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        GraphBase.__init__(self, name=name)
        Dictable.__init__(self, data=data)

    def nodes(self) -> list[Node]:
        """
        ========================================================================
         Return List of Nodes in the Graph.
        ========================================================================
        """
        return list(self.values())

    def clone(self) -> Self:
        """
        ========================================================================
         Return a Cloned object.
        ========================================================================
        """
        data = {key: node.clone() for key, node in self.data.items()}
        return GraphDict(data=data, name=self.name)

    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return the neighbors of a node.
        ========================================================================
        """
        raise NotImplementedError("Not implemented for GraphDict")

    def key_comparison(self) -> dict[Key, Node]:
        """
        ========================================================================
         Return a Key-Comparison object.
        ========================================================================
        """
        return self.data
