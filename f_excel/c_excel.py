import openpyxl as xl
from openpyxl.styles import PatternFill, Font, Alignment
import openpyxl.styles.colors as Colors
from openpyxl.styles.borders import Border, Side
from f_utils import u_file


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
        self.wb = None
        if u_file.is_exists(filename):
            self.wb = xl.load_workbook(filename=filename)
        else:
            self.wb = xl.Workbook()
        self.ws = self.wb.worksheets[index_ws]

    def set_value(self, row, col, value):
        """
        ========================================================================
         Description: Set Value in Cell by Row and Col numbers.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. row : int
            2. col : int
            3. value : obj
        ========================================================================
        """
        assert type(row) == int
        assert type(col) == int
        assert row >= 1
        assert col >= 1
        self.ws.cell(row=row, column=col).value = value

    def get_value(self, row, col):
        """
        ========================================================================
         Description: Return Value in the Cell by Row and Col numbers.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. row : int
            2. col : int
        ========================================================================
         Return: obj
        ========================================================================
        """
        return self.ws.cell(row, col).value

    def set_font(self, row, col, color='000000', is_bold=False):
        font = Font(color=color, bold=is_bold, vertAlign='baseline')
        self.ws.cell(row, col).font = font
        self.ws.cell(row, col).alignment = Alignment(horizontal='center',
                                                     vertical='center')

    def set_background(self, row, column, color):
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
            border = Border(left=Side(style=style),
                            right=Side(style=style),
                            top=Side(style=style),
                            bottom=Side(style=style))
        self.ws.cell(row, column).border = border

    def clear_cells(self, row, col, row_last=None, col_last=None,
                    rows=1, cols=1):
        """
        ========================================================================
         Description: Clear the Cell (Value, Background, Borders).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. row : int (First Row).
            2. col : int (First Col).
            3. row_last : int (Equals to Row on None).
            4. col_last : int (Equals to Col on None).
            5. rows : int (Amount of Rows).
            6. cols : int (Amount of Cols).
        ========================================================================
        """
        if not row_last:
            row_last = row + rows - 1
        if not col_last:
            col_last = col + cols - 1
        for r in range(row, row_last+1):
            for c in range(col, col_last+1):
                self.set_value(r, c, value=str())
                self.set_background(r, c, color='WHITE')
                self.set_border(r, c, style='thin')

    def merge_cells(self, row, col, row_last=None, col_last=None,
                    rows=1, cols=1):
        """
        ========================================================================
         Description: Merge Cells.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. row : int (First Row).
            2. col : int (First Col).
            3. row_last : int (Equals to Row on None).
            4. col_last : int (Equals to Col on None).
            5. rows : int (Amount of Rows).
            6. cols : int (Amount of Cols).
        ========================================================================
        """
        if not row_last:
            row_last = row + rows - 1
        if not col_last:
            col_last = col + cols - 1
        self.ws.merge_cells(start_row=row, start_column=col,
                            end_row=row_last, end_column=col_last)

    def set_column_width(self, col):
        self.ws.column_dimensions[col] = 4

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
