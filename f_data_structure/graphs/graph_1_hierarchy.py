from f_data_structure.nodes.node_1_hierarchical import NodeHierarchical
from f_data_structure.graphs.graph_0_nodes import GraphNodes


class GraphHierarchy(GraphNodes):
    """
    ============================================================================
     Represents Graph of Hierarchical-Nodes (have Parent and Children).
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. children(node: NodeHierarchy) -> list[NodeHierarchy]
           [*] Returns Node's children (neighbors that are not parent).
    ============================================================================
      Inherited Methods:
    ----------------------------------------------------------------------------
        1. add_node(node: Node) -> None
           [*] Adds a new Node to the Graph.
        2. add_edge(node_a: Node, node_b: Node) -> None
           [*] Adds a new Edge in the Graph between the two given Nodes.
        3. nodes() -> List[Node]
           [*] Returns a List of Graph's Nodes in Insertion-Order.
    ============================================================================
    """

    # Dict mapping Nodes to their Neighbors
    _nodes: dict[NodeHierarchical: list[NodeHierarchical]]

    def children(self, node: NodeHierarchical) -> list[NodeHierarchical]:
        """
        ========================================================================
         Returns a given Node's Children (neighbors that are not parent).
        ========================================================================
        """
        return [child
                for child
                in self.neighbors(node)
                if not child == node.parent]
