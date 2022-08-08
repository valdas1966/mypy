from f_logging.dec import log_all_methods, log_info_class
from f_excel.model.wb.base import MyExcelWorkBookBase
from f_excel.ws import MyExcelWorkSheet


@log_all_methods(decorator=log_info_class)
class MyExcelWorkBookSheets(MyExcelWorkBookBase):
    """
    ============================================================================
     Description:
    ----------------------------------------------------------------------------
        1. Represents the Excel-Workbook file.
        2. Can make a copy of a WorkSheet.
        3. Can return a MyExcelWorkSheet object by its Title or Index.
    ============================================================================
    """

    def __init__(self, xlsx: str):
        """
        ========================================================================
         Description: Run the super().
        ========================================================================
        """
        super().__init__(xlsx=xlsx)

    def get_worksheet(self,
                      title: str = None,
                      index: int = 0) -> MyExcelWorkSheet:
        """
        ========================================================================
         Description: Return Excel-WorkSheet Object by its Title or Index.
        ========================================================================
        """
        try:
            if title:
                ws = self._wb[title]
            else:
                ws = self._wb.worksheets[index]
            return MyExcelWorkSheet(ws=ws)
        except Exception as e:
            self.close()
            raise Exception(e)

    def copy_worksheet(self, title_src: str, title_dest: str) -> None:
        """
        ========================================================================
         Description: Make a Copy of an Excel-WorkSheet. Gets the names of the
                       source and the destination WorkSheet (to create). If the
                       destination WorkSheet exists, the file will become
                       corrupted.
        ========================================================================
        """
        try:
            src = self._wb[title_src]
            dest = self._wb.copy_worksheet(src)
            dest.title = title_dest
        except Exception as e:
            self._wb.close()
            raise Exception(e)
