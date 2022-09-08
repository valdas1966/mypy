import time
from f_utils import u_file
import openpyxl as xl
from f_excel.wb import MyWorkBook

xlsx = 'd:\\temp\\temp.xlsx'
n_rows = 10000
n_cols = 1
value = 999


def run_openpyxl():
    u_file.delete(xlsx)
    wb = xl.Workbook()
    ws = wb.worksheets[0]
    for row in range(n_rows):
        for col in range(n_cols):
            cell = ws.cell(row+1, col+1)
            cell.value = value
    wb.save(xlsx)


def run_myexcel():
    u_file.delete(xlsx)
    wb = MyWorkBook(xlsx)
    for row in range(n_rows):
        for col in range(n_cols):
            wb[row+1, col+1].value = value
    wb.close()


def measure(func: 'func') -> float:
    time_start = time.time()
    func()
    return time.time() - time_start


def measure_avg(func: 'func', n: int = 3) -> float:
    seconds = [measure(func) for _ in range(n)]
    avg = sum(seconds) / len(seconds)
    print(f'{avg}: {str(func)}')


measure_avg(run_openpyxl)
measure_avg(run_myexcel)
