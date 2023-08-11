from f_excel.inner.wb.i_1_open_save_close import MyWorkBookOpenSaveClose
from f_excel.inner.ws.ws import MyWorkSheet


class MyWorkBookSheets(MyWorkBookOpenSaveClose):
    """
    ============================================================================
     Description:
    ----------------------------------------------------------------------------
        2. Can make a copy of a WorkSheet.
        3. Can return a MyExcelWorkSheet object by its Title or Index.
    ============================================================================
    """

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
                      Raise Exception if the input is not int|str.
        ========================================================================
        """
        if type(item) == str:
            return MyWorkSheet(self._wb[item])
        elif type(item) == int:
            return MyWorkSheet(self._wb.worksheets[item])
        else:
            raise TypeError(f'Expected int|str, {type(item)} was given ')
