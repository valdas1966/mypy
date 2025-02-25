from f_ds.nodes.i_2_cell import NodeCell, Cell


class GenNodeCell:
    """
    ========================================================================
     Generate a NodeCell.
    ========================================================================
    """

    @staticmethod
    def by_row_col(row: int, col: int) -> NodeCell:
        """
        ========================================================================
         Generate a NodeCell by Row and Column.
        ========================================================================
        """
        cell = Cell(row=row, col=col)
        return NodeCell(uid=cell)
