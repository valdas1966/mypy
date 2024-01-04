from f_google.utils import u_auth
from f_abstract.mixins.nameable import Nameable
from gspread.client import Client
from gspread.spreadsheet import Spreadsheet
import gspread


class SpreadSheet(Nameable):
    """
    ============================================================================
     Google-SpreadSheet Class.
    ============================================================================
    """

    _paths:  dict = {'valdas': 'd:\\temp\\2023\\12\\gsheet.json'}

    def __init__(self, id_spread_sheet: str, name: str = 'valdas') -> None:
        """
        ========================================================================
         Init the Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        self._id_spread_sheet = id_spread_sheet
        self._client: Client = None
        self._spread_sheet: Spreadsheet = None

    @property
    def id_spread_sheet(self) -> str:
        return self._id_spread_sheet

    def open(self) -> None:
        """
        ========================================================================
         Open the Google-SpreadSheet.
        ========================================================================
        """
        path_json = self._paths[self.name]
        creds = u_auth.get_credentials(path_json=path_json)
        self._client = gspread.authorize(creds)
        self._spread_sheet = self._client.open_by_key(self._id_spread_sheet)
