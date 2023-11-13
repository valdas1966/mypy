from f_data_structure.f_tree.node import Node


class Graph:

    def __init__(self,
                 nodes: list[Node] = list(),
                 edges: dict[Node, list[Node]] = dict()) -> None:
        self._nodes = nodes
        self._edges = edges

    @property
    # Graph's Nodes
    def nodes(self) -> list[Node]:
        return self._nodes

    @property
    # Graph's Edges
    def edges(self) -> dict[Node, list[Node]]:
        return self._edges

    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return Node's Neighbors.
        ========================================================================
        """
        return self._edges[node]
