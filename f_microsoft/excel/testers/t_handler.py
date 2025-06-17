from f_microsoft.excel.generators.g_excel import GenExcel, Excel
from f_os.u_file import UFile


def test_open_new_file() -> None:
    """
    ========================================================================
     Test the open-new-file functionality.
    ------------------------------------------------------------------------
      1. Delete file if it exists
      2. Create a new file
      4. Check if file exists (really created)
      5. Delete file (clean-up)
    ========================================================================
    """
    # Path to the Excel file to test
    path = 'g:\\test.xlsx'
    # Create an empty file
    excel = GenExcel.empty(path=path)
    # Close the file
    excel.close()
    # Test that the file was created
    assert UFile.is_exists(path)
    # Delete file (clean-up)
    UFile.delete(path)


def test_open_existing_file() -> None:
    """
    ========================================================================
     Test the open-existing-file functionality.
    ========================================================================
    """
    # Path to the Excel file to test
    path = 'g:\\test.xlsx'
    # Create new file
    excel = GenExcel.empty(path=path)
    # Close file
    excel.close()
    # Open the file
    excel = Excel(path=path)
    # Close the file
    excel.close()
    # Delete file (clean-up)
    UFile.delete(path)
