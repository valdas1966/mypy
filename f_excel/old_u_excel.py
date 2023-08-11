from old_c_excel import Excel
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


def filter(xlsx_main, xlsx_sub, col, fr, val):
    """
    ============================================================================
     Description: Filter out rows by Value in given Column.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. xlsx_main : str (Path to existed Excel-File)
        2. xlsx_sub : str (Path to Excel-File to Create)
        3. col : int (Column to Check)
        4. fr : int (First Row)
        5. val : str (Value to Check)
    ============================================================================
    """
    row = fr
    excel = Excel(xlsx_main)
    cur_val = excel.get_value(row, col)
    while cur_val:
        if cur_val != val:
            excel.delete_row(row)
        else:
            row = row + 1
        cur_val = excel.get_value(row, col)
    excel.save_as(xlsx_sub)
    excel.close()


def divide_by_col_val(xlsx, col, fr):
    """
    ============================================================================
     Description: Divide Excel-File into group of Excel-Files by Column Values.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. xlsx : str (Path to Main Excel-File).
        2. col : str (Column Name to divide by it).
        3. fr : int (First Row to check).
    ============================================================================
    """
    values = col_to_set(xlsx, col, fr)
    for val in values:
        xlsx_new = u_file.replace_filename(xlsx, f'{val}.xlsx')
        filter(xlsx, xlsx_new, col, fr, val)
