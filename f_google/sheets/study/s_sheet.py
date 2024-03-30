from f_google.sheets.client import GSheets
from datetime import datetime

# The Sheet must be shared to the Client-Email (Ivan)
id_spread = '1LqiT2mBYlo1i2M6tabj8s9kiEHngffg4dYY7-amPbgw'

sheet = GSheets.spread(user='VALDAS', id_spread=id_spread)[0]
print(sheet.index)
print(sheet.title)
print()

sheet[1, 1].value = str(datetime.now())
print(sheet[1, 1])
sheet.update()
print(sheet[1, 1])

print(sheet.last_row(col=1))
