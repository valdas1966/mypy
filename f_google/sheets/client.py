import gspread
from f_google.utils import u_auth


class Client:
    """
    ============================================================================
     Google-Sheets Client.
    ============================================================================
    """

    # Mapping Users to their JSONs
    _paths: dict = {'valdas': 'd:\\temp\\2023\\12\\gsheet.json'}

    def __init__(self, user: str = 'valdas'):
        """
        ========================================================================
         Init Private Attributes.
        ========================================================================
        """
        self._user = user
        path_json = self._paths[user]
        creds = u_auth.get_credentials(path_json=path_json)
        self._client = gspread.authorize(creds)

    @property
    def user(self) -> str:
        return self._user

    @property
    def client(self) -> gspread.client.Client:
        return self._client

    def get_spread(self, id_spread: str) -> gspread.spreadsheet:
        """
        ========================================================================
         Return a Spreadsheet Class by its ID.
        ========================================================================
        """
        return self._client.open_by_key(key=id_spread)
