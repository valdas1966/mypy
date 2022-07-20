from f_logging.dec import log_all_methods, log_info_class
import openpyxl as xl
from f_utils import u_file
from f_excel.model.xl_worksheet import MyExcelWorkSheet


#@log_all_methods(decorator=log_info_class)
class MyExcelWorkBook:

    def __init__(self, xlsx: str):
        """
        ========================================================================
         Description: Constructor. Open new or existed Excel-File for editing.
        ========================================================================
        """
        # Path to XL-File
        self._xlsx = xlsx
        # Working Excel-WorkBook
        self._wb = self.__set_workbook()

    def get_worksheet(self,
                      title: str = None,
                      index: int = 0) -> 'MyExcelWorkSheet':
        """
        ========================================================================
         Description: Return Excel-WorkSheet Object by its Title or Index.
        ========================================================================
        """
        try:
            ref = title if title else index
            ws = self._wb.worksheets[ref]
            return MyExcelWorkSheet(wb=self, ws=ws)
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

    def save(self) -> None:
        """
        ========================================================================
         Description: Save the Excel-File.
        ========================================================================
        """
        self._wb.save(self._xlsx)

    def save_as(self, xlsx_new: str) -> None:
        """
        ========================================================================
         Description: Save the Excel-File as other name. Delete the (other)
                       file if it exists.
        ========================================================================
        """
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
            self.save()
        self._wb.close()

    def __set_workbook(self) -> xl.Workbook:
        """
        ========================================================================
         Description: Set the Working Excel WorkBook. If the Excel path-file is
                        passed to the Constructor, then open it for editing.
                        Otherwise, create and open a new blank Excel-File.
        ========================================================================
        """
        if u_file.is_exists(self._xlsx):
            return xl.load_workbook(filename=self._xlsx, keep_vba=True)
        return xl.Workbook()
