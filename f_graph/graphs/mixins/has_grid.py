from f_graph.node import NodeGraph
from f_ds.grids.grid import Grid, Cell
from typing import Generic, TypeVar, Type

Node = TypeVar('Node', bound=NodeGraph[Cell])


class HasGrid(Generic[Node]):

    def __init__(self, grid: Grid) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._grid = grid


