from c_excel import Excel
from f_utils import u_file


def col_to_set(xlsx, col, fr):
    """
    ============================================================================
     Description: Convert Excel-Column into Set of Values.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. xlsx : str (Excel FilePath).
        2. col : int (Column Index).
        3. fr : int (First Row).
    ============================================================================
     Return: set
    ============================================================================
    """
    excel = Excel(xlsx)
    s = excel.col_to_set(col, fr)
    excel.close()
    return s


def filter(xlsx_old, xlsx_new, col, fr, val):
    """
    ============================================================================
     Description: Filter out rows that in given Column are not equal
                    to given Value.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. xlsx_old : str (Path to existed Excel-File)
        2. xlsx_new : str (Path to Excel-File to Create)
        3. col : int (Column to Check)
        4. fr : int (First Row)
        5. val : str (Value to Check)
    ============================================================================
    """
    row = fr
    excel = Excel(xlsx_old)
    cur_val = excel.get_value(row, col)
    while cur_val:
        if cur_val == val:
            excel.delete_row(row)
        else:
            row = row + 1
        cur_val = excel.get_value(row, col)
    excel.save_as(xlsx_new)
    excel.close()


def divide_by_col_val(xlsx_old, col, fr):
    """
    ============================================================================
     Description: Divide Excel-File into group of Excel-Files by Column Values.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
    :param path:
    :param xlsx_old:
    :param col:
    :param fr:
    :return:
    """
    excel = Excel(xlsx_old)
    values = excel.col_to_set(col, fr)
    excel.close()
    for val in values:
        xlsx_new = u_file.replace_filename(xlsx_old, f'{val}.xlsx')
        filter(xlsx_old, xlsx_new, col, fr, val)


