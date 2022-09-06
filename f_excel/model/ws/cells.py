import openpyxl.worksheet
from f_excel.model.ws.base import MyWorkSheetBase
from f_excel.cell import MyCell


class MyWorkSheetCells(MyWorkSheetBase):

    def __init__(self, ws: openpyxl.worksheet):
        super().__init__(ws=ws)

    def __getitem__(self, item: tuple[int, int]) -> any:
        """
        ========================================================================
         Description: Return the MyCell by the given coordinates (Row, Col).
        ========================================================================
        """
        row, col = item
        cell = self._ws.cell(row, col)
        return MyCell(cell=cell)
