from f_excel.c_excel_map import ExcelMap


excel_test = 'D:\\Temp\\test.xlsx'

xl_map = ExcelMap(excel_test)
xl_map.set_blocks(row=3, col=3)
xl_map.set_blocks(row=5, col=5, col_last=9)
xl_map.set_blocks(row=7, col=5, rows=5, cols=5)
xl_map.close()
