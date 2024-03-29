from f_google.sheets.client import GSheets


gs = GSheets(user='VALDAS')

print(type(gs._client))
