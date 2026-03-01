from f_google.bigquery.main import BigQuery


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
        return BigQuery()
