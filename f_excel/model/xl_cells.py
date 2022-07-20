from model.xl_worksheet import MyExcelWorkSheet


class MyExcelCells:

    def __init__(self, ws: MyExcelWorkSheet):
        """
        ========================================================================
         Description: Constructor. Set the Current Excel-WorkSheet.
        ========================================================================
        """
        self._ws = ws

    def __setitem__(self, key: tuple, value) -> None:
        """
        ========================================================================
         Description: Set the Value to the Cell. The Cell is represented by the
                        tuple (key) of row and col indeces.
        ========================================================================
        """
        row, col = key
        self._ws.cells(row=row, column=col).value = value

    def __getitem__(self, item):
        row, col = item
        return self._ws.cells(row=row, column=col).value
