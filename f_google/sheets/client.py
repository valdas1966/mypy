import gspread
from f_google.utils import u_auth
from f_google.sheets.spread import Spread


class Client:
    """
    ============================================================================
     Google-Sheets Client.
    ============================================================================
    """

    # Mapping Users to their JSONs
    class JSon:
        VALDAS = 'd:\\temp\\2023\\12\\gsheet.json'
        GCP = 'GCP'

    def __init__(self, json: str = JSon.GCP):
        """
        ========================================================================
         Init Private Attributes.
        ========================================================================
        """
        self._json = json
        creds = u_auth.get_credentials(path_json=json)
        self._client: gspread.client.Client = gspread.authorize(creds)

    @property
    def json(self) -> str:
        return self._json

    def open_spread(self, id_spread: str) -> Spread:
        """
        ========================================================================
         Return a Spreadsheet Class by its ID.
        ========================================================================
        """
        spread: gspread.spreadsheet = self._client.open_by_key(key=id_spread)
        return Spread(id_spread=id_spread, spread=spread)
