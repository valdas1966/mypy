from f_google.bigquery.main import BigQuery
from f_google.auth import Auth


class Factory:
    """
    ============================================================================
     Factory for BigQuery Client.
    ============================================================================
    """

    @staticmethod
    def rami() -> BigQuery:
        """
        ========================================================================
         Return a BigQuery Client for the RAMI Service Account.
        ========================================================================
        """
        creds = Auth.Factory.rami()
        return BigQuery(creds=creds)
