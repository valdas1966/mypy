from old_old_f_google.services.sheets.client import GSheets, Spread


class UGSheets:
    """
    ============================================================================
     Google-Sheets Utils-Class.
    ============================================================================
    """

    @staticmethod
    def spread(user: str, id_spread: str) -> Spread:
        """
        ========================================================================
         1. Open GSheets-Client by a given User.
         2. Return SpreadSheet by a given Id-Spread.
        ========================================================================
        """
        gs = GSheets(user=user)
        return gs.open_spread(id_spread=id_spread)
