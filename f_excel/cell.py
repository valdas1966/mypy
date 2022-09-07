from f_excel.model.cell.value import MyCellValue
import openpyxl


class MyCell(MyCellValue):

    def __init__(self, cell: openpyxl.cell.cell.Cell):
        super().__init__(cell=cell)
