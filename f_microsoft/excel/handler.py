from f_microsoft.excel.components.layout import Layout
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl import Workbook, load_workbook
from f_file.i_0_handler import FileHandler


class Excel(FileHandler):
    """
    ============================================================================
     Excel file handler.
    ============================================================================
    """

    def __init__(self,
                 # Path to the Excel file to be opened
                 path: str
                 ) -> None:
        """
        ========================================================================
         Initialize the Excel file handler.
        ========================================================================
        """
        self._wb: Workbook = None
        self._sheet: Worksheet = None
        self._layout: Layout = None
        FileHandler.__init__(self, path=path)
    
    @property
    def layout(self) -> Layout:
        """
        ========================================================================
         Get the layout of the worksheet.
        ========================================================================
        """
        return self._layout

    def set_cell_value(self,
                       # Row index
                       row: int,
                       # Column index
                       col: int,
                       # Value
                       value: str) -> None:
        """
        ========================================================================
         Set the value of a cell.
        ========================================================================
        """
        self._sheet.cell(row=row, column=col).value = value

    def save(self) -> None:
        """
        ========================================================================
         Save the Excel file.
        ========================================================================
        """
        self._wb.save(self.path)

    def save_as(self, path: str) -> None:
        """
        ========================================================================
         Save the Excel file to a new path.
        ========================================================================
        """
        self._wb.save(path)

    def close(self, save: bool = True) -> None:
        """
        ========================================================================
         Close the Excel file.
        ========================================================================
        """
        if save:
            self.save()
        self._wb.close()
        
    def _create(self) -> None:
        """
        ========================================================================
         Create a new Excel file.
        ========================================================================
        """
        self._wb = Workbook()
        self.save()

    def _open(self) -> None:
        """
        ========================================================================
         Open an existing Excel file.
        ========================================================================
        """
        self._wb = load_workbook(self.path)
        self._sheet = self._wb.active
        self._layout = Layout(sheet=self._sheet)
