from f_ds.graphs.i_2_grid import GraphGrid
from f_graph.path.node import NodePath
from f_ds.grids.grid import Grid
from typing import TypeVar, Type

Node = TypeVar('Node', bound=NodePath)


class GraphPath(GraphGrid[Node]):
    """
    ============================================================================
     Graph for Path-Finding problems.
    ============================================================================
    """

    def __init__(self,
                 grid: Grid,
                 type_node: Type[Node] = NodePath,
                 name: str = None) -> None:
        """
        ========================================================================
         Initialize the Graph.
        ========================================================================
        """
        GraphGrid.__init__(self, grid=grid, type_node=type_node, name=name)

    def children(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return List of Node's Neighbors that are not its parents.
        ========================================================================
        """
        return [child
                for child
                in self.neighbors(node=node)
                if (not node.parent or node.parent != child)]
