from f_google.sheets.sheet import Sheet

# The Sheet must be shared to the Client-Email (Ivan)
id_sheet = '1LqiT2mBYlo1i2M6tabj8s9kiEHngffg4dYY7-amPbgw'
s = Sheet(id_sheet=id_sheet)
s.open()
s.close()
