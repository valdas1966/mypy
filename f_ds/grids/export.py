from __future__ import annotations
from typing import TYPE_CHECKING
from f_ds.groups.group import Group
from f_ds.grids.grid import Cell
import numpy as np


if TYPE_CHECKING:
    # Only used for type hints  
    from f_ds.grids.grid import Grid


class Export:
    """
    ============================================================================
     Export-Grid class.
    ============================================================================
    """

    def __init__(self, grid: Grid) -> None:
        """
        ========================================================================
         Initialize the Export-Grid.
        ========================================================================
        """
        self._grid = grid

    def group(self, name: str = None) -> Group[Cell]:
        """
        ========================================================================
         Return a flattened list representation of the Grid.
        ========================================================================
        """
        return Group(name=name, data=list(self._grid))
    
    def array(self) -> np.ndarray:
        """
        ========================================================================
         Return a numpy boolean array representation of the Grid.
        ========================================================================
        """
        return np.array([[bool(cell) for cell in row]
                        for row in self._grid._cells])