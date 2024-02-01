from f_google.sheets.client import Client
from f_google.sheets.spread import Spread
from f_google.sheets.sheet import Sheet

# The Sheet must be shared to the Client-Email (Ivan)
id_spread = '1LqiT2mBYlo1i2M6tabj8s9kiEHngffg4dYY7-amPbgw'

client = Client(json=Client.JSon.VALDAS)
spread = client.open_spread(id_spread=id_spread)
sheet = spread[0]
print(sheet.index)
print(sheet.title)

cell = sheet[1, 1]
cell.value = 'Hello1'
print(cell.value)
sheet.update()
print(sheet[2, 1].value)
