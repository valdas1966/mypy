from f_graph.graphs.i_1_dict import GraphDict, UID
from f_graph.path.nodes.i_1_cell import NodePath
from typing import TypeVar

Node = TypeVar('Node', bound=NodePath)


class GraphPath(GraphDict[Node, UID]):
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
