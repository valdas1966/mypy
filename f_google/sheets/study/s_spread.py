from f_google.sheets.client import GSheets


# The SpreadSheet must be shared to the Client-Email (Ivan)
id_spread = '1LqiT2mBYlo1i2M6tabj8s9kiEHngffg4dYY7-amPbgw'

spread = GSheets.spread(user='VALDAS', id_spread=id_spread)
print(spread.titles())
