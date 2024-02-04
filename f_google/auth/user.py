from frozendict import frozendict


class User:
    """
    ============================================================================
     Google-User.
    ============================================================================
    """

    # Paths to JSon-Keys to Google Account
    _JSONS = frozendict({'VALDAS': 'd:\\temp\\2023\\12\\gsheet.json',
                        'GCP': None})

    def __init__(self, user: str) -> None:
        self._user = user

    @property
    def user(self) -> str:
        return self._user

    def path_json(self) -> str:
        """
        ========================================================================
         Return Path to Json-Key of the Google-Account.
        ========================================================================
        """
        return self._JSONS[self._user]
