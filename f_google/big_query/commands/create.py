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
              tname: str,
              schema: Schema) -> None:
        """
        ========================================================================
         Create list table by the received Col Names and Types.
        ========================================================================
        """
        self._drop.table(tname=tname)
        table = Table(table_ref=tname, schema=schema.to_schema_fields())
        self._client.create_table(table=table,
                                  retry=Retry())
        if self._verbose:
            print(f'Table [{tname}] has been created.')
            print(f'Schema:')
            for field in schema:
                print(f'  - {field.dtype}: {field.name}')
