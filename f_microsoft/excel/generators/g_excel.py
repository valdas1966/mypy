from f_microsoft.excel.handler import Excel
from f_os.u_file import UFile


class GenExcel:
    """
    ============================================================================
     Excel file generator.
    ============================================================================
    """

    @staticmethod
    def empty(path: str) -> Excel:
        """
        =======================================================================
         Generate an empty Excel file.
        =======================================================================
        """
        # Delete file if it exists
        UFile.delete(path)
        # Create new file
        return Excel(path=path)