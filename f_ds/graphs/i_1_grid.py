from f_ds.graphs.i_0_base import GraphBase
from f_ds.graphs.nodes.i_2_cell import NodeCell
from f_ds.grids.grid import Grid
from typing import TypeVar

Node = TypeVar('Node', bound=NodeCell)


class GraphGrid(GraphBase[Node]):
    """
    ============================================================================
     Graph represents 2D-Grid.
    ============================================================================
    """

    def __init__(self, grid: Grid, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        GraphBase.__init__(self, name)
        self._grid = grid

    @property
    def grid(self) -> Grid:
        return self._grid

    def nodes(self) -> list[Node]:
        return list(self._grid)
