from f_excel.model.xl_workbook import MyExcelWorkBook
from f_excel.model.xl_worksheet import MyExcelWorkSheet

xlsx = 'd:\\temp\\test_3.xlsx'
wb = MyExcelWorkBook(xlsx=xlsx)
ws = wb.get_worksheet()
ws.set_title(title='x')
wb.close(to_save=True)
