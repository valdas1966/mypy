from f_logging.dec import log_all_methods, log_info_class
from f_excel.model.wb.base import MyWorkBookBase
from f_excel.ws import MyWorkSheet


@log_all_methods(decorator=log_info_class)
class MyWorkBookSheets(MyWorkBookBase):
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

    def __getitem__(self, item: int | str) -> MyWorkSheet:
        """
        ========================================================================
         Description: Return MyWorkSheet by Index(int) or Title(str).
                      Raise Exception if argument[item] in not int|str.
        ========================================================================
        """
        if type(item) == str:
            return MyWorkSheet(self._wb[item])
        elif type(item) == int:
            return MyWorkSheet(self._wb.worksheets[item])
        else:
            raise Exception(f'EXCEPTION! Expected: [str, int], Given: '
                            f'[{type(item)}]')
