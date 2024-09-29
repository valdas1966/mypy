from f_graph.graphs.i_0_base import GraphBase, NodeBase
from typing import TypeVar

Node = TypeVar('Node', bound=NodeBase)


class GraphMutable(GraphBase[Node]):
    """
    ============================================================================
     Mutable-Graph.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 nodes: dict[Node, list[Node]] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        GraphBase.__init__(self, name)
        self._nodes = nodes if nodes else dict()

    def nodes(self) -> list[Node]:
        """
        ========================================================================
         Return List of Nodes in the Graph.
        ========================================================================
        """
        return list(self._nodes.keys())

    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Returns List of list given Node's neighbors.
        ========================================================================
        """
        return self._nodes[node]

    def to_list(self) -> list[Node]:
        """
        ========================================================================
         Return list list representation of the Object.
        ========================================================================
        """
        return self.nodes()
