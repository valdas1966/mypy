from openpyxl.styles import PatternFill
import openpyxl.styles.colors as colors
from f_excel.c_excel import Excel


filename = 'D:\\Temp\\temp_1.xlsx'

xl = Excel(filename)
xl.fill_cell(row=1, column=1, name_color='RED')
xl.fill_cell(row=2, column=1, name_color='YELLOW')
xl.fill_cell(row=3, column=1, name_color='GREEN')
xl.close()

"""
for i in range(64):
    color = PatternFill(start_color=colors.COLOR_INDEX[i],
                        end_color=colors.COLOR_INDEX[i],
                        fill_type='solid')
    xl.fill_cell(row=i+1, column=1, color=color)
"""