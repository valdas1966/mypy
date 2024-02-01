from f_google.sheets.client import Client
from f_google.sheets.spread import Spread
from f_google.sheets.sheet import Sheet


class SheetQA:

    _id_spread = '1mOhkn4DPpUlgtuQxzTPNWlymBSmq9fS7T0t3IaDFf98'

    def __init__(self) -> None:
        client = Client(json=Client.JSon.VALDAS)
        spread: Spread = client.open_spread(id_spread=self._id_spread)
        _sheet: Sheet = spread[0]
