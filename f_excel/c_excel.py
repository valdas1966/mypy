import openpyxl as xl
from openpyxl.styles import PatternFill
import openpyxl.styles.colors as Colors
from openpyxl.styles.borders import Border, Side


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

    def set_value(self, row, column, value):
        self.ws.cell(row=row, column=column).value = value

    def set_color_back(self, row, column, color):
        fill = Excel.color_excel(color)
        self.ws.cell(row=row, column=column).fill = fill

    def set_border(self, row, column, style='thick'):
        """
        ========================================================================
         Description: Set Block on specified Cell.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. row : int (Cell's Row).
            2. column : int (Cell's Column).
            3. style : str ('thick' | 'thin' | None).
        ========================================================================
        """
        border = None
        if style:
            border = Border(left=Side(style), right=Side(style),
                            top=Side(style), bottom=Side(style))
        self.ws.cell(row, column).border = border

    def close(self):
        """
        ========================================================================
         Description: Save and Close the Workbook.
        ========================================================================
        """
        self.wb.save(self.filename)
        self.wb.close()

    @staticmethod
    def color_excel(name_color):
        """
        ========================================================================
         Description: Get Color's Name and return its Excel PatternFill.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. name_color : str (Color's Name).
        ========================================================================
        """
        enum = {'BLACK': 0, 'WHITE': 1, 'YELLOW': 51, 'GREEN': 57, 'RED': 60,
                'GRAY': 55}
        color = Colors.COLOR_INDEX[enum[name_color]]
        return PatternFill(start_color=color,
                           end_color=color,
                           fill_type='solid')
