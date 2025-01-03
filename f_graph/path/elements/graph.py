from f_graph.elements.graphs.i_2_grid import GraphGrid
from f_graph.path.elements.node import NodePath
from typing import TypeVar

Node = TypeVar('Node', bound=NodePath)


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
