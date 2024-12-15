from f_google.services.sheets.client import GSheets


gs = GSheets(user='VALDAS')

print(type(gs._client))
