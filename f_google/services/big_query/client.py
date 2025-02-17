from google.cloud.bigquery import Client
from f_google.client.base import ClientBase
from f_google.user import User
from f_google.services.big_query.commands.drop import Drop
from f_google.services.big_query.commands.create import Create
from f_google.services.big_query.commands.insert import Insert
from f_google.services.big_query.commands.select import Select


class BigQuery(ClientBase):
    """
    ============================================================================
     Google Big-Query Client.
    ============================================================================
    """

    def __init__(self,
                 user: str = User.RAMI,
                 verbose: bool = True) -> None:
        ClientBase.__init__(self, user=user)
        self._drop = Drop(client=self._client,
                          verbose=verbose)
        self._create = Create(client=self._client,
                              verbose=verbose,
                              drop=self._drop)
        self._insert = Insert(client=self._client)
        self._select = Select(client=self._client)
        if verbose:
            print(f'Connected to BigQuery Project [{self.creds.project_id}] '
                  f'as [{user}].')

    @property
    def drop(self) -> Drop:
        return self._drop

    @property
    def create(self) -> Create:
        return self._create

    @property
    def insert(self) -> Insert:
        return self._insert

    @property
    def select(self) -> Select:
        return self._select

    def _get_client(self) -> Client:
        """
        ========================================================================
         Open and list Return list BigQuery Client.
        ========================================================================
        """
        return Client(credentials=self.creds)
