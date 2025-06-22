from old_f_google.services.sheets.client import GSheets


ID_SPREAD = '1haZi5T98P6kq3dnq4dO10JHDql-179B1oVluxQ_CW2M'


spread = GSheets.spread(user='VALDAS', id_spread=ID_SPREAD)

print(type(spread))

