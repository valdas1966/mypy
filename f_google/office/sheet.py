from f_google.utils import u_auth
from f_abstract.mixins.nameable import Nameable
from gspread.client import Client
from gspread.spreadsheet import Spreadsheet
import gspread


class Sheet(Nameable):
    """
    ============================================================================
     Google-Sheet Class.
    ============================================================================
    """

    _paths:  dict = {'valdas': 'd:\\temp\\2023\\12\\gsheet.json'}

    def __init__(self, id_sheet: str, name: str = 'valdas') -> None:
        Nameable.__init__(self, name=name)
        self._id_sheet = id_sheet
        self._client: Client = None
        self._sheet: Spreadsheet = None

    @property
    def id_sheet(self) -> str:
        return self._id_sheet

    def open(self) -> None:
        """
        ========================================================================
         Open the Google Sheet.
        ========================================================================
        """
        path_json = self._paths[self.name]
        creds = u_auth.get_credentials(path_json=path_json)
        self._client = gspread.authorize(creds)
        self._sheet = self._client.open_by_key(self._id_sheet)
