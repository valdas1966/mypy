from f_excel.model.wb.wb import MyExcelWorkBook

repo = 'd:\\temp'
xlsx = f'{repo}\\test_5.xlsx'
wb = MyExcelWorkBook(xlsx=xlsx)
ws = wb.get_worksheet()
cell_1 = ws[1, 1]
cell_1.value = 1
cell_2 = ws[1, 1]
print(cell_2.value)
print(cell_2.is_empty())
cell_2.empty()
print(cell_2.is_empty())
wb.close(to_save=True)
