from f_data_structure.inner.grid.i_0_init import GridInit
from f_data_structure.old_cell import Cell


class GridContent(GridInit):

    def elements(self) -> list[Cell]:
        """
        ========================================================================
         Desc: Return List of Grid's Elements.
        ========================================================================
        """
        return [e for row in self._grid for e in row]
