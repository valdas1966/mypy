from f_microsoft.excel.generators import GenExcel, Excel
from f_os.u_file import UFile


def test_set_row_height() -> None:
    """
    ========================================================================
     Test the layout functionality.
    ========================================================================
    """
    path = 'g:\\test.xlsx'         # Path to the Excel file to test
    row = 1                        # Row index to test
    height_new = 20                # Row height new
    # Create new file
    excel = GenExcel.empty(path=path)
    # Test that the row height is the default
    assert excel.layout.height_row[row] == excel.layout.height_row.DEFAULT
    # Set row height
    excel.layout.height_row[row] = height_new
    # Test that the row height is the new
    assert excel.get_height_row(row=row) == height_new
    # Close file (clean-up)
    excel.close()
    # Delete file
    UFile.delete(path)


def test_set_col_width() -> None:
    """
    ========================================================================
     Test the set-col-width functionality.
    ========================================================================
    """
    path = 'g:\\test.xlsx'         # Path to the Excel file to test
    col = 1                        # Column index to test
    width_new = 20                 # Column width new
    # Create new file
    excel = GenExcel.empty(path=path)
    # Test that the column width is the default
    assert excel.get_width_col(col=col) == 13
    # Set column width
    excel.set_width_col(col=col, width=width_new)
    # Test that the column width is the new
    assert excel.get_width_col(col=col) == width_new
    # Close file (clean-up)
    excel.close()
    # Delete file
    UFile.delete(path)