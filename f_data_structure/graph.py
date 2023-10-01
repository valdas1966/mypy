from f_data_structure.nodes.node_0_base import NodeBase as Node


class Graph:

    nodes: dict[Node: list[Node]]

    def __init__(self) -> None:
        self._nodes = dict()

    @property
    def nodes(self) -> list:
        """
        ========================================================================
         Returns a list of Graph's Nodes in the Insertion-Order.
        ========================================================================
        """
        return list(self._nodes.keys())

    def add_node(self, node: Node) -> None:
        """
        ========================================================================
         Adds a new Node into the Graph.
        ========================================================================
        """
        self._nodes[node] = list()

    def add_edge(self, node_a: Node, node_b: Node) -> None:
        """
        ========================================================================
         Adds a new Edge in a Graph between two given Nodes.
        ========================================================================
        """
        self._nodes[node_a].append(node_b)

    def neighbors(self, node: Node) -> list[Node]:
        return self._nodes[node]

    def children(self, node: Node) -> list[Node]:
        return [child
                for child
                in self.neighbors(node)
                if not child == node.parent]

