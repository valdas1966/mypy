from f_graph.graphs.i_2_grid import GraphGrid
from f_ds.nodes.i_1_heuristic import NodeHeuristic
from typing import TypeVar

Node = TypeVar('Node', bound=NodeHeuristic)


class GraphPath(GraphGrid[Node]):
    """
    ============================================================================
     Graph for Path-Finding problems.
    ============================================================================
    """

    def children(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return List of Node's Neighbors that are not its parents.
        ========================================================================
        """
        return [child
                for child
                in self.neighbors(node=node)
                if child.parent != node]
