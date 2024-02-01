from f_google.sheets.client import Client
from f_google.sheets.spread import Spread


# The SpreadSheet must be shared to the Client-Email (Ivan)
id_spread = '1LqiT2mBYlo1i2M6tabj8s9kiEHngffg4dYY7-amPbgw'

client = Client(user='valdas')
spread = client.open_spread(id_spread=id_spread)
print(spread.titles())
