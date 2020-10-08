import openpyxl as xl
from openpyxl.styles import PatternFill
import openpyxl.styles.colors as Colors


class Excel:
    """
    ============================================================================
     Description: Class for working with Microsoft Excel.
    ============================================================================
    """

    def __init__(self, filename, index_ws=0):
        """
        ========================================================================
         Description: Constructor. Open Excel Workbook and Worksheet.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. filename : str (Excel Filename to open).
            2. index_ws : int (Index of the Worksheet in Excel File).
        ========================================================================
        """
        self.filename = filename
        self.wb = xl.load_workbook(filename=filename)
        self.ws = self.wb.worksheets[index_ws]

    def write_value(self, row, column, value):
        self.ws.cell(row=row, column=column).value = value

    def fill_cell(self, row, column, name_color):
        fill = Excel.color_excel(name_color)
        self.ws.cell(row=row, column=column).fill = fill

    def close(self):
        self.wb.save(self.filename)
        self.wb.close()

    @staticmethod
    def color_excel(name_color):
        enum = {'BLACK': 0, 'WHITE': 1, 'YELLOW': 51, 'GREEN': 57, 'RED': 60,
                'GRAY': 55}
        color = Colors.COLOR_INDEX[enum[name_color]]
        return PatternFill(start_color=color,
                           end_color=color,
                           fill_type='solid')
