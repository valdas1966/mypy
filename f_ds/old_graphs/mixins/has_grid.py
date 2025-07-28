from f_graph.elements.node import NodeGraph
from f_ds.old_grids.old_grid import Grid, Cell
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeGraph[Cell])


class HasGrid(Generic[Node]):

    def __init__(self, grid: Grid) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._grid = grid



