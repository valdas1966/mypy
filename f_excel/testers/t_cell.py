from f_utils import u_tester
from f_excel.wb import MyWorkBook


class TesterCell:

    repo = 'd:\\temp'
    xlsx = f'{repo}\\test.xlsx'

    def __init__(self):
        u_tester.print_start(__file__)
        TesterWorkBook.__tester_base()
        TesterWorkBook.__tester_sheets()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_base():
        """
        ========================================================================
         Description: Check the following processes:
        ------------------------------------------------------------------------
            1. Open-New-File by a FilePath.
            2. Save the current File.
            3. Save-As current file by a new FilePath.
            4. Close the current file.
        ========================================================================
        """
        xlsx_1 = TesterWorkBook.xlsx_1
        xlsx_2 = TesterWorkBook.xlsx_2
        u_file.delete([xlsx_1, xlsx_2])
        xl = MyWorkBook(xlsx=xlsx_1)
        xl.save()
        xl.save_as(xlsx_new=xlsx_2)
        xl.close()
        p0 = u_file.is_exists(xlsx_1)
        p1 = u_file.is_exists(xlsx_2)
        try:
            xl_1 = MyWorkBook(xlsx=xlsx_1)
            xl_1.close()
            p2 = True
        except FileNotFoundError:
            p2 = False
        try:
            xl_2 = MyWorkBook(xlsx=xlsx_2)
            xl_2.close()
            p3 = True
        except FileNotFoundError:
            p3 = False
        u_tester.msg('[Open-New-File by Filepath][Save][Save-As][Close]')
        u_tester.run(p0, p1, p2, p3)

    @staticmethod
    def __tester_sheets():
        """
        ========================================================================
         Description: Check the following processes:
        ------------------------------------------------------------------------
            1. Return MyWorkSheets by Index(int)|Title(str).
            2. Copy WorkSheet in the WorkBook.
        ========================================================================
        """
        xl = MyWorkBook(xlsx=TesterWorkBook.xlsx)
        ws_1 = xl[0]
        ws_1.title = 'src'
        xl.copy_worksheet(title_src='src', title_dest='dest')
        ws_2 = xl['dest']
        p0 = True
        try:
            ws_3 = xl[True]
            p0 = False
        except Exception as e:
            p0 = True
        xl.close()
        p1 = type(ws_1) == MyWorkSheet
        p2 = type(ws_2) == MyWorkSheet
        u_tester.msg('[Return MyWorkSheets only by Index(int)|Title(str)][Copy '
                     'WorkSheet]')
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TesterWorkBook()
