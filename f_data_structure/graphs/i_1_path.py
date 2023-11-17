from f_data_structure.graphs.i_0_graph import Graph
from f_data_structure.nodes.i_1_path import NodePath as Node
from collections import defaultdict


class GraphPath(Graph):
    """
    ============================================================================
     Path-Based Graph.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 nodes: defaultdict[Node, list[Node]] = None) -> None:
        Graph.__init__(self, name, nodes)

    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return Neighbors that are not Node's Parent (avoid cycles).
        ========================================================================
        """
        return [n
                for n
                in Graph.neighbors(self, node)
                if n != node.parent]
