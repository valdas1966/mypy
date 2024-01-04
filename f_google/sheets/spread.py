from gspread.spreadsheet import Spreadsheet
from f_google.sheets.client import Client


class Spread:

    def __init__(self,
                 id_spread: str,
                 user: str = 'valdas'):
        self._id_spread = id_spread
        self._client = Client(user=user)
        self._spread: Spreadsheet = self._client.get_spread(id_spread)

    @property
    def id_spread(self) -> str:
        return self._id_spread

    def stam(self) -> None:
        pass