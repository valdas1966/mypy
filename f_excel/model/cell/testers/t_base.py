from f_excel.model.wb.wb import MyExcelWorkBook

repo = 'd:\\temp'
xlsx = f'{repo}\\test_5.xlsx'
wb = MyExcelWorkBook(xlsx=xlsx)
ws = wb.get_worksheet()
cell = ws[2, 4]
print(cell.row, cell.col)
wb.close(to_save=True)
