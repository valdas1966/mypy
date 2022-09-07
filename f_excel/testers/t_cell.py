from f_utils import u_tester, u_file
from f_excel.wb import MyWorkBook


class TesterMyCell:

    repo = 'd:\\temp'
    xlsx = f'{repo}\\test.xlsx'

    def __init__(self):
        u_tester.print_start(__file__)
        TesterMyCell.__tester_base()
        TesterMyCell.__tester_value()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_base():
        """
        ========================================================================
         Test:
        ------------------------------------------------------------------------
            1. Return Cell's coordinates (Row and Col).
        ========================================================================
        """
        row = 1
        col = 2
        u_file.delete(TesterMyCell.xlsx)
        xl = MyWorkBook(xlsx=TesterMyCell.xlsx)
        cell = xl[0][row, col]
        xl.close()
        p0 = cell.row == row
        p1 = cell.col == col
        u_tester.msg('[Return Cell Coordinates]')
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_value():
        """
        ========================================================================
         Test:
        ------------------------------------------------------------------------
            1. Set|Get Value.
            2. Empty|Is_Empty Value.
        ========================================================================
        """
        row_full = 1
        col_full = 2
        row_empty = 3
        col_empty = 4
        value = 12
        u_file.delete(TesterMyCell.xlsx)
        xl = MyWorkBook(xlsx=TesterMyCell.xlsx)
        cell_full = xl[0][row_full, col_full]
        cell_empty = xl[0][row_empty, col_empty]
        xl.close()
        cell_full.value = value
        p0 = cell_full.value == value
        p1 = cell_empty.is_empty()
        p2 = not cell_full.is_empty()
        cell_full.empty()
        p3 = cell_full.is_empty()
        u_tester.msg('[Set|Get Value][Empty|Is Empty Value]')
        u_tester.run(p0, p1, p2, p3)


if __name__ == '__main__':
    TesterMyCell()
