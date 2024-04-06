from f_google.sheets.client import GSheets
from datetime import datetime

# The Sheet must be shared to the Client-Email (Ivan)
id_spread = '1LqiT2mBYlo1i2M6tabj8s9kiEHngffg4dYY7-amPbgw'

sheet = GSheets.spread(user='VALDAS', id_spread=id_spread)[0]


def study_get_and_set():
    print(sheet.index)
    print(sheet.title)
    print()

    sheet[1, 1].value = str(datetime.now())
    print(sheet[1, 1])
    sheet.update()
    print(sheet[1, 1])


def study_get_row_last():
    # Col to Study
    col_study = 2
    # Cells to Study (3, 2) is Empty and not studied
    cell_a = sheet[1, col_study]
    cell_b = sheet[2, col_study]
    cell_c = sheet[4, col_study]
    # Reset the Cells
    cell_a.value = str()
    cell_b.value = str()
    cell_c.value = str()
    sheet.update()
    # Col is Empty so Print -1 (no full cell)
    print(sheet.get_row_last(col=col_study))
    # Fill the Cells to Study
    cell_a.value = 1
    cell_b.value = 1
    cell_c.value = 1
    sheet.update()
    # Last Full-Cell is in Row 2 (First-Row=1)
    print(sheet.get_row_last(col=col_study))
    # Last Full-Cell is in Row 4 (First-Row=4)
    print(sheet.get_row_last(col=col_study, row_first=cell_c.row))


def study_to_tuples():
    # Cols to Study
    col_first = 3
    col_last = 4
    # Row First
    row_first = 1
    # Fill Cells to Study
    sheet[1, col_first].value = 1
    sheet[1, col_last].value = 2
    sheet[2, col_first].value = 3
    sheet[2, col_last].value = 4
    sheet.update()
    # Convert the Range into Tuple of Tuples
    tuples = sheet.to_tuples(col_first, col_last, row_first)
    for i, t in enumerate(tuples):
        print(i, t[0], t[1])


#study_get_row_last()
study_to_tuples()
