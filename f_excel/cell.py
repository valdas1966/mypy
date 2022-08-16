from f_excel.model.cell.base import MyCellBase
import openpyxl


class MyCell(MyCellBase):

    def __init__(self, cell: openpyxl.cell.cell.Cell):
        super().__init__(cell=cell)
