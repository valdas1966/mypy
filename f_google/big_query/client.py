from google.cloud.bigquery import Client
from f_google.client.base import ClientBase
from f_google.big_query.commands.drop import Drop
from f_google.big_query.commands.create import Create
from f_google.big_query.commands.select import Select


class BigQuery(ClientBase):
    """
    ============================================================================
     Google Big-Query Client.
    ============================================================================
    """

    def __init__(self,
                 user: str,
                 verbose: bool = True) -> None:
        ClientBase.__init__(self, user=user)
        Client.__init__(self,
                        project=self.creds.project_id,
                        credentials=self.creds)
        self._drop = Drop(client=self, verbose=verbose)
        self._create = Create(client=self, verbose=verbose, drop=self._drop)
        self._select = Select(client=self)
        if verbose:
            print(f'Connected to BigQuery Project [{self.creds.project_id}] '
                  f'as [{user}]')

    @property
    def drop(self) -> Drop:
        return self._drop

    @property
    def create(self) -> Create:
        return self._create

    @property
    def select(self) -> Select:
        return self._select
