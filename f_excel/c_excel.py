import openpyxl as xl


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

    def close(self):
        self.wb.save(filename)
        self.wb.close()


filename = 'D:\\Temp\\temp_1.xlsx'
excel = Excel(filename)
excel.write_value(1,1,100)
excel.write_value(2,1,200)
excel.write_value(3,1,300)
excel.close()

#end
