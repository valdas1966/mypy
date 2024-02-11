from google.cloud.bigquery import Table, Client
from f_google.strategies.retry import Retry
from f_google.big_query.abc.command import Command
from f_google.big_query.commands.drop import Drop
from f_google.big_query.structures.schema import Schema


class Create(Command):
    """
    ============================================================================
     BigQuery Create-Commands.
    ============================================================================
    """

    def __init__(self,
                 client: Client,
                 verbose: bool,
                 drop: Drop) -> None:
        Command.__init__(self, client=client, verbose=verbose)
        self._drop = drop

    def table(self,
              name: str,
              schema: Schema) -> None:
        """
        ========================================================================
         Create a table by the received Col Names and Types.
        ========================================================================
        """
        self._drop.table(name=name)
        table = Table(table_ref=name, schema=schema.build())
        table.
        self._client.create_table(table=table,
                                  retry=Retry())
        print(f'Table [{name}] has been created.')

