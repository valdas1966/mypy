from f_data_structure.nodes.node_0_hierarchy import NodeBase as Node


class Graph:
    """
    ============================================================================
     Represents a simple Graph with Nodes and Edges.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. add_node(node: Node) -> None
           [*] Adds a new Node to the Graph.
        2. add_edge(node_a: Node, node_b: Node) -> None
           [*] Adds a new Edge in the Graph between the two given Nodes.
        3. nodes() -> List[Node]
           [*] Return a List of Graph's Nodes in Insertion-Order.
        4. neighbors(node: Node) -> list[Node]
           [*] Returns a List of Neighbors for a given Node
        5. children(node: Node) -> List[Node]
           [*] Returns Node's Children (Neighbors that are not Parent).
    ============================================================================
    """

    _nodes: dict[Node: list[Node]]    # Dict mapping Nodes to their Neighbors

    def __init__(self) -> None:
        """
        ========================================================================
         Initializes the private dictionary.
        ========================================================================
        """
        self._nodes = dict()

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
         Adds a new Node to the Graph.
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
        """
        ========================================================================
         Returns a List of a given Node's neighbors.
        ========================================================================
        """
        return self._nodes[node]

    def children(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Returns a List of a Node's children (neighbors that are not parent).
        ========================================================================
        """
        return [child
                for child
                in self.neighbors(node)
                if not child == node.parent]
