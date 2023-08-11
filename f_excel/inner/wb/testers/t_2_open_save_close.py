from f_utils import u_tester, u_file
from f_excel.inner.wb.i_1_open_save_close import MyWorkBookOpenSaveClose
import zipfile
import os


class TesterOpenSaveClose:
    """
    ============================================================================
     Test:
    ----------------------------------------------------------------------------
        1. Open New-Excel-File.
        2. Save Excel-File.
        3. Open Existed-Excel-File.
        4. Save-As Excel-File.
        5. Close Excel-File.
    ============================================================================
    """

    repo = f'{os.getcwd()[0]}:\\temp'
    xlsx_1 = f'{repo}\\test_1.xlsx'
    xlsx_2 = f'{repo}\\test_2.xlsx'
    xlsx_invalid = f'{repo}\\test_invalid.xlsx'

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_open_new_file()
        self.__tester_save_file()
        self.__tester_open_existed_file()
        self.__tester_save_as_file()
        self.__tester_close_file()
        u_tester.print_finish(__file__)

    def __tester_open_new_file(self):
        xl = MyWorkBookOpenSaveClose()
        xl.close()
        u_tester.run(True)

    def __tester_save_file(self):
        u_file.delete(self.xlsx_1)
        xl = MyWorkBookOpenSaveClose(xlsx=self.xlsx_1)
        xl.save()
        xl.close()
        u_tester.run(True)

    def __tester_open_existed_file(self):
        # Valid Excel-File
        u_file.delete(self.xlsx_1)
        xl = MyWorkBookOpenSaveClose(xlsx=self.xlsx_1)
        xl.close()
        p0 = True
        # Invalid Excel-File
        p1 = False
        u_file.write(path=self.xlsx_invalid, text=str())
        try:
            MyWorkBookOpenSaveClose(xlsx=self.xlsx_invalid)
        except zipfile.BadZipfile:
            p1 = True
        u_tester.run(p0, p1)

    def __tester_save_as_file(self):
        xl = MyWorkBookOpenSaveClose(xlsx=self.xlsx_1)
        xl.save_as(xlsx_new=self.xlsx_2)
        xl.close()
        xl = MyWorkBookOpenSaveClose(xlsx=self.xlsx_2)
        xl.close()
        u_tester.run(True)

    def __tester_close_file(self):
        xl = MyWorkBookOpenSaveClose(xlsx=self.xlsx_1)
        xl.close()
        u_tester.run(True)


if __name__ == '__main__':
    TesterOpenSaveClose()
