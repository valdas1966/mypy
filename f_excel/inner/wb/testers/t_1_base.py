from f_utils import u_tester, u_file
from f_excel.inner.wb.i_1_base import MyWorkBookBase


class TesterWorkBook:
    """
    ============================================================================
     Test:
    ----------------------------------------------------------------------------
        1. Open New-Excel-File.
        2. Save Excel-File.
        3. Open Existed-Excel-File.
        4. Close Excel-File.
    ============================================================================
    """

    repo = 'd:\\temp'
    xlsx_1 = f'{repo}\\test_1.xlsx'
    xlsx_2 = f'{repo}\\test_2.xlsx'

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_open_new_file()
        self.__tester_save_file()
        self.__tester_open_existed_file()
        self.__tester_save_as_file()
        self.__tester_close_file()
        u_tester.print_finish(__file__)

    def __tester_open_new_file(self):
        u_file.delete(self.xlsx_1)
        xl = MyWorkBookBase(xlsx=self.xlsx_1)
        p0 = True
        u_tester.run(p0)
        xl.close()

    def __tester_save_file(self):
        xl = MyWorkBookBase(xlsx=self.xlsx_1)
        xl.save()
        p0 = True
        u_tester.run(p0)
        xl.close()

    def __tester_open_existed_file(self):
        xl = MyWorkBookBase(xlsx=self.xlsx_1)
        p0 = True
        u_tester.run(p0)
        xl.close()

    def __tester_save_as_file(self):
        xl = MyWorkBookBase(xlsx=self.xlsx_1)
        xl.save_as(xlsx_new=self.xlsx_2)
        xl.close()
        xl = MyWorkBookBase(xlsx=self.xlsx_2)
        p0 = True
        u_tester.run(p0)
        xl.close()

    def __tester_close_file(self):
        xl = MyWorkBookBase(xlsx=self.xlsx_1)
        xl.close()
        p0 = True
        u_tester.run(p0)


if __name__ == '__main__':
    TesterWorkBook()
