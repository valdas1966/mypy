from f_excel.old_c_excel_map import ExcelMap
from f_map.c_map import Map

excel_test = 'D:\\Temp\\test.xlsx'

xl_map = ExcelMap(excel_test)
xl_map.clear_cells(row=1, col=1, rows=100, cols=100)
map = Map(rows=5, obstacles=20)
map.draw_excel(xl_map, row_start=2, col_start=2, title='Map 001')
# xl_map.set_blocks(row=3, col=3)
# xl_map.set_blocks(row=5, col=5, col_last=9)
# xl_map.set_blocks(row=7, col=5, rows=5, cols=5)
xl_map.close()
