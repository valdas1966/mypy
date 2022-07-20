from f_excel.model.xl_workbook import MyExcelWorkBook

repo = 'd:\\temp'
xlsx_1 = f'{repo}\\test_1.xlsx'
xlsx_2 = f'{repo}\\test_2.xlsx'

xl = MyExcelWorkBook(xlsx=xlsx_1)
xl.save()
xl.save_as(xlsx_new=xlsx_2)
xl.close()
