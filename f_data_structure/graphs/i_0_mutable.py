from f_data_structure.graphs.abc.base import GraphBase
from f_data_structure.nodes.i_0_base import NodeBase as Node
from collections import defaultdict


class GraphMutable(GraphBase):
    """
    ============================================================================
     Graph with Nodes and Edges.
    ============================================================================
    """

    # Dict mapping Nodes to their Neighbors
    _nodes: defaultdict[Node, list[Node]]

    def __init__(self,
                 name: str = None,
                 nodes: defaultdict[Node, list[Node]] = None) -> None:
        """
        ========================================================================
         Initialize the private dictionary.
        ========================================================================
        """
        GraphBase.__init__(self, name)
        self._nodes = defaultdict(list, nodes or {})

    def nodes(self) -> list[Node]:
        """
        ========================================================================
         Returns a list of Graph's Nodes in the Insertion-Order.
        ========================================================================
        """
        return list(self._nodes.keys())

    def add_node(self, node: Node) -> None:
        """
        ========================================================================
         Adds a new Node to the Graph.
        ========================================================================
        """
        self._nodes[node]

    def add_edge(self, node_a: Node, node_b: Node) -> None:
        """
        ========================================================================
         Adds a new Edge in a Graph between two given Nodes.
        ========================================================================
        """
        self._nodes[node_a].append(node_b)
        self._nodes[node_b].append(node_a)

    def get_neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Returns a List of a given Node's neighbors.
        ========================================================================
        """
        return self._nodes[node]