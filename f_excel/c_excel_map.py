from f_excel.c_excel import Excel


class ExcelMap(Excel):

    def set_blocks(self, row, col, row_last=None, col_last=None,
                   rows=1, cols=1):
        """
        ========================================================================
         Description: Get Square of Coordinates and set Cells as Block.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. row : int
        ========================================================================
        """
        if not row_last:
            row_last = row + rows - 1
        if not col_last:
            col_last = col + cols - 1
        for r in range(row, row_last+1):
            for c in range(col, col_last+1):
                self.__set_block(r, c)

    def __set_block(self, row, col):
        """
        ========================================================================
         Description: Get Coordinates and set Cell as Block.
        ========================================================================
            1. row : int (start from 1).
            2. col : int (start from 1).
        ========================================================================
        """
        self.set_value(row, col, value=str())
        self.set_background(row, col, color='BLACK')
        self.set_border(row, col, style='thick')
