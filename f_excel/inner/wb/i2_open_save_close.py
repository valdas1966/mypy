from f_excel.inner.wb.i1_init import MyWorkBookInit
import openpyxl as xl
from f_utils import u_file


class MyWorkBookOpenSaveClose(MyWorkBookInit):
    """
    ============================================================================
     Description:
    ----------------------------------------------------------------------------
        1. Open New or Existed Excel-File (by path).
        2. Save or Save-As the Excel-File.
        3. Close the Excel-File.
    ============================================================================
    """

    def __init__(self, xlsx: str = None) -> None:
        """
        ========================================================================
         Description: Constructor. Open new or existed Excel-File for editing.
        ========================================================================
        """
        assert isinstance(xlsx, str) or xlsx is None, type(xlsx)
        super().__init__(xlsx=xlsx)
        self._wb = self.__set_workbook()

    def __del__(self):
        """
        ========================================================================
         Description: Destructor. Close the Excel-WorkBook.
        ========================================================================
        """
        try:
            self.close()
        except AttributeError:
            pass

    def save(self) -> None:
        """
        ========================================================================
         Description: Save the Excel-File.
        ========================================================================
        """
        if self._xlsx:
            self._wb.save(filename=self._xlsx)

    def save_as(self, xlsx_new: str) -> None:
        """
        ========================================================================
         Description: Save the Excel-File as other name. Delete the (other)
                       file if it exists.
        ========================================================================
        """
        assert type(xlsx_new) == str, type(xlsx_new)
        try:
            if u_file.is_exists(xlsx_new):
                u_file.delete(xlsx_new)
            self._wb.save(xlsx_new)
        except Exception as e:
            self.close()
            raise Exception(e)

    def close(self, to_save: bool = False) -> None:
        """
        ========================================================================
         Description: Close (and optionally save) the Excel-File.
        ========================================================================
        """
        if to_save:
            try:
                self.save()
            except (TypeError, FileNotFoundError):
                pass
        if self._wb:
            self._wb.close()

    def __set_workbook(self) -> xl.Workbook:
        """
        ========================================================================
         Description: Set the Working Excel WorkBook. If the Excel path-file is
                        passed to the Constructor, then open it for editing.
                        Otherwise, create and open a new blank Excel-File.
        ========================================================================
         Raise: InvalidFileException if xlsx exists and invalid.
        ========================================================================
        """
        if u_file.is_exists(self._xlsx):
            return xl.load_workbook(filename=self._xlsx)
        return xl.Workbook()
