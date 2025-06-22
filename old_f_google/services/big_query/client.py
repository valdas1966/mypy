from google.cloud.bigquery import Client
from old_f_google.client.base import ClientBase
from old_f_google.user import User
from old_f_google.services.big_query.commands.drop import Drop
from old_f_google.services.big_query.commands.create import Create
from old_f_google.services.big_query.commands.insert import Insert
from old_f_google.services.big_query.commands.select import Select
from old_f_google.services.big_query.commands.alter import Alter
from old_f_google.services.big_query.commands.truncate import Truncate


class BigQuery(ClientBase):
    """
    ============================================================================
     Google Big-Query Client.
    ============================================================================
    """

    def __init__(self,
                 user: str = User.RAMI,
                 verbose: bool = True) -> None:
        """
        ========================================================================
         Initialize the BigQuery Client.
        ========================================================================
        """
        ClientBase.__init__(self, user=user)
        self._drop = Drop(client=self._client,
                          verbose=verbose)
        self._create = Create(client=self._client,
                              verbose=verbose,
                              drop=self._drop)
        self._insert = Insert(client=self._client)
        self._select = Select(client=self._client)
        self._alter = Alter(client=self._client,
                            verbose=verbose)
        self._truncate = Truncate(client=self._client,
                                  verbose=verbose)
        if verbose:
            print(f'Connected to BigQuery Project [{self.creds.project_id}] '
                  f'as [{user}].')

    @property
    def drop(self) -> Drop:
        """
        ========================================================================
         Return the Drop Command.
        ========================================================================
        """
        return self._drop

    @property
    def create(self) -> Create:
        """
        ========================================================================
         Return the Create Command.
        ========================================================================
        """
        return self._create

    @property
    def insert(self) -> Insert:
        """
        ========================================================================
         Return the Insert Command.
        ========================================================================
        """
        return self._insert

    @property
    def select(self) -> Select:
        """
        ========================================================================
         Return the Select Command.
        ========================================================================
        """
        return self._select

    @property
    def alter(self) -> Alter:
        """
        ========================================================================
         Return the Alter Command.
        ========================================================================
        """
        return self._alter
    
    @property
    def truncate(self) -> Truncate:
        """
        ========================================================================
         Return the Truncate Command.
        ========================================================================
        """
        return self._truncate

    def _get_client(self) -> Client:
        """
        ========================================================================
         Open and list Return list BigQuery Client.
        ========================================================================
        """
        return Client(credentials=self.creds)
