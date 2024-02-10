from f_google.big_query.abc.command import Command
from f_google.big_query.structures.schema import Schema
from f_google.strategies.retry import Retry
from google.cloud.bigquery import Table


class Create(Command):
    """
    ============================================================================
     BigQuery Create-Commands.
    ============================================================================
    """

    def table(self,
              name: str,
              schema: Schema) -> None:
        """
        ========================================================================
         Create a table by the received Col Names and Types.
        ========================================================================
        """
        table = Table(table_ref=name, schema=schema.build())
        self._client.create_table(table=table,
                                  exists_ok=True,
                                  retry=Retry())
