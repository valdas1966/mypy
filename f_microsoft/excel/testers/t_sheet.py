from f_color.rgb import RGB
from f_microsoft.excel.generators.g_excel import GenExcel, Excel
from f_os.u_file import UFile


def test_sheet_title() -> None:
    """
    ========================================================================
     Test the title of the sheet.
    ========================================================================
    """
    # Path to the Excel file to test
    path = 'g:\\test.xlsx'
    
    # Generate an empty Excel and change the first sheet's title to 'Test'
    excel = GenExcel.empty(path=path)
    sheet = excel[1]
    sheet.title = 'Test'
    excel.close()

    # Open the modified Excel and assert the first sheet's title
    excel = Excel(path=path)
    title = excel[1].title
    excel.close()
    UFile.delete(path=path)
    assert title == 'Test'


def test_sheet_row() -> None:
    """
    ========================================================================
     Test the row of the sheet.
    ========================================================================
    """
    # Path to the Excel file to test
    path = 'g:\\test.xlsx'
    
    # Generate an empty Excel and change the first sheet's row height to 10
    excel = GenExcel.empty(path=path)
    sheet = excel[1]
    sheet.row[1].height = 10
    excel.close()

    # Open the modified Excel and assert the first sheet's row height
    excel = Excel(path=path)
    sheet = excel[1]
    height = sheet.row[1].height
    excel.close()
    UFile.delete(path=path)
    assert height == 10


def test_sheet_col() -> None:
    """
    ========================================================================
     Test the column of the sheet.
    ========================================================================
    """
    # Path to the Excel file to test
    path = 'g:\\test.xlsx'
    
    # Generate an empty Excel and change the first sheet's column width to 10
    excel = GenExcel.empty(path=path)
    sheet = excel[1]
    sheet.col[1].width = 10
    excel.close()

    # Open the modified Excel and assert the first sheet's column width
    excel = Excel(path=path)
    sheet = excel[1]
    width = sheet.col[1].width
    excel.close()           
    assert width == 10

    # Clean up
    UFile.delete(path=path)


def test_sheet_set_rows_and_cols_layout() -> None:
    """
    ========================================================================
     Test the set_rows_height and set_cols_width methods of the sheet.
    ========================================================================
    """
    # Path to the Excel file to test
    path = 'g:\\test.xlsx'

    # Generate an empty Excel and set the rows and columns layout
    excel = GenExcel.empty(path=path)
    sheet = excel[1]
    sheet.set_rows_height(rows=[2, 3, 4], height=54)
    sheet.set_cols_width(cols=[2, 3, 4], width=10)
    excel.close()

    # Open the modified Excel and assert the rows and columns layout
    excel = Excel(path=path)
    sheet = excel[1]
    assert sheet.row[2].height == 54
    assert sheet.row[3].height == 54
    assert sheet.row[4].height == 54
    assert sheet.col[2].width == 10
    assert sheet.col[3].width == 10
    assert sheet.col[4].width == 10
    excel.close()

    # Clean up
    UFile.delete(path=path)


def test_cell_background() -> None:
    """
    ========================================================================
     Test the background of the cell.
    ========================================================================
    """
    # Path to the Excel file to test
    path = 'g:\\test.xlsx'

    # Generate an empty Excel and set the background of the cell
    excel = GenExcel.empty(path=path)
    sheet = excel[1]
    cell = sheet[1][1]
    rgb_red = RGB(r=1, g=0, b=0)
    cell.background = rgb_red
    excel.close()

    # Open the modified Excel and assert the background of the cell
    excel = Excel(path=path)
    sheet = excel[1]
    cell = sheet[1][1]
    assert cell.background == rgb_red
    excel.close()

    # Clean up
    # UFile.delete(path=path)


