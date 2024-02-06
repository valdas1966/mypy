from google.cloud import bigquery
from f_google.client.base import ClientBase


class Client(ClientBase):
    """
    ============================================================================
     Google Big-Query Client.
    ============================================================================
    """

    def _open_client(self):
        """
        ========================================================================
         Open and Return a BigQuery-Client.
        ========================================================================
        """
        return bigquery.Client(credentials=self.creds,
                               project=self.creds.project_id)
