from old_f_google.services.sheets.client import GSheets


# The SpreadSheet must be shared to the Client-Email (gsheet@natural-nimbus...)
id_spread = '1LqiT2mBYlo1i2M6tabj8s9kiEHngffg4dYY7-amPbgw'
id_spread = '1mOhkn4DPpUlgtuQxzTPNWlymBSmq9fS7T0t3IaDFf98'

spread = GSheets.spread(user='VALDAS', id_spread=id_spread)
print(spread.titles())
