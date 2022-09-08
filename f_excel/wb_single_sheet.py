from f_logging.dec import log_all_methods, log_info_class
from f_excel.model.wb.base import MyWorkBookBase


@log_all_methods(decorator=log_info_class)
class MyWorkBookSingleSheet(MyWorkBookBase):

    def __getitem__(self, item: tuple[int, int]) -> any:
        """
        ========================================================================
         Description: Return the MyCell by the given coordinates (Row, Col) of
                        the first WorkSheet.
        ========================================================================
        """
        return
        row, col = item
        cell = self._ws.cell(row, col)
        return MyCell(cell=cell)