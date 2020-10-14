from openpyxl.styles import PatternFill
import openpyxl.styles.colors as colors
from f_excel.c_excel import Excel


filename = 'D:\\Temp\\temp_1.xlsx'

xl = Excel(filename)
xl.set_color_back(row=1, column=1, color='RED')
xl.set_color_back(row=2, column=1, color='YELLOW')
xl.set_color_back(row=3, column=1, color='GREEN')
xl.set_border(row=17, column=2, style='thick')
xl.set_block(row=17, column=2)
xl.close()

"""
for i in range(64):
    color = PatternFill(start_color=colors.COLOR_INDEX[i],
                        end_color=colors.COLOR_INDEX[i],
                        fill_type='solid')
    xl.fill_cell(row=i+1, column=1, color=color)
"""