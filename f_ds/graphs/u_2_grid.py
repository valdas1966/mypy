from f_ds.graphs.i_2_grid import GraphGrid, NodeGraph
from f_ds.old_grids.u_grid import UGrid
from typing import Generic, TypeVar, Type

Node = TypeVar('Node', bound=NodeGraph)


class UGraphGrid(Generic[Node]):
    """
    ============================================================================
     Utils-Class of Graph-Grid.
    ============================================================================
    """

    @staticmethod
    def gen(rows: int,
            cols: int = None,
            pct_valid: int = 100,
            type_node: Type[Node] = NodeGraph,
            name: str = None) -> GraphGrid:
        """
        ========================================================================
         Return a generated GraphGrid by received parameters.
        ========================================================================
        """
        grid = UGrid.gen(rows=rows, cols=cols, pct_valid=pct_valid)
        return GraphGrid(grid=grid, name=name, type_node=type_node)

    @staticmethod
    def gen_3x3(type_node: Type[Node] = NodeGraph,
                name: str = None) -> GraphGrid:
        """
        ========================================================================
         Return a Full-Valid GraphGrid of 3x3 dimension.
        ========================================================================
        """
        return UGraphGrid.gen(rows=3, type_node=type_node, name=name)

