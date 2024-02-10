from google.cloud import bigquery
from f_google.client.base import ClientBase
from f_google.big_query.commands.select import Select
from f_google.big_query.commands.create import Create


class Client(ClientBase):
    """
    ============================================================================
     Google Big-Query Client.
    ============================================================================
    """

    def __init__(self, user: str) -> None:
        ClientBase.__init__(self, user=user)
        self._create = Create(client=self._client)
        self._select = Select(client=self._client)

    @property
    def create(self) -> Create:
        return self._create

    @property
    def select(self) -> Select:
        return self._select

    def _open_client(self) -> bigquery.Client:
        """
        ========================================================================
         Open and Return a BigQuery-Client.
        ========================================================================
        """
        return bigquery.Client(credentials=self.creds,
                               project=self.creds.project_id)
