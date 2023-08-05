from f_data_structure.f_grid.grid_layout import GridLayout


class GridCelss(GridLayout):

    def cells(self) -> list[XYAble]:
        """
        ========================================================================
         Desc: Return List of Grid's Elements.
        ========================================================================
        """
        return [e for row in self._grid for e in row if self.is_valid(xy=e)]