from f_google.services.sheets.spread.main import Spread
from f_google.creds.oauth import OAuth
from f_google.creds.auth import Auth


class Factory:
    """
    ============================================================================
     Factory for Google Spreadsheet.
    ============================================================================
    """

    @staticmethod
    def valdas(id_spread: str) -> Spread:
        """
        ====================================================================
         Return a Spread Client for VALDAS OAuth Credentials.
        ====================================================================
        """
        creds = OAuth.Factory.valdas()
        return Spread(creds=creds, id_spread=id_spread)

    @staticmethod
    def valdas_test() -> Spread:
        id_spread = '1LqiT2mBYlo1i2M6tabj8s9kiEHngffg4dYY7-amPbgw'
        return Factory.valdas(id_spread=id_spread)

    @staticmethod
    def rami(id_spread: str) -> Spread:
        """
        ====================================================================
         Return a Spread Client for RAMI Service-Account Credentials.
        ====================================================================
        """
        creds = Auth.Factory.rami()
        return Spread(creds=creds, id_spread=id_spread)
