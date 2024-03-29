from f_google.sheets.client import GSheets

# The Sheet must be shared to the Client-Email (Ivan)
id_spread = '1LqiT2mBYlo1i2M6tabj8s9kiEHngffg4dYY7-amPbgw'

sheet = GSheets.spread(user='VALDAS', id_spread=id_spread)[0]
print(sheet.index)
print(sheet.title)
print()

cell = sheet[1, 1]
cell.value = 'Hello1'
print(cell.value)
cell.value = 'Hello2'
print(sheet[1, 1].value)
sheet.update()
print(sheet[1, 1].value)
