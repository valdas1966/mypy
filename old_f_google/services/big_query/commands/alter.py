from google.cloud.bigquery import Table, Client, SchemaField
from google.api_core.exceptions import NotFound
from old_f_google.strategies.retry import Retry
from old_f_google.services.big_query.abc.command import Command
from old_f_google.services.big_query.structures.schema import Schema


class Alter(Command):
    """
    ============================================================================
     BigQuery Alter-Commands (e.g., Add Column).
    ============================================================================
    """

    def __init__(self,
                 # Google BigQuery Client
                 client: Client,
                 # Verbose Mode
                 verbose: bool) -> None:
        """
        ========================================================================
         Initialize the Alter Command.
        ========================================================================
        """
        Command.__init__(self, client=client, verbose=verbose)

    def add_col(self,
                # Table Name
                name_table: str,
                # Column Name
                name_col: str,
                # Column Type
                type_col: str) -> None:
        """
        ========================================================================
         Add a column to a table.
        ========================================================================
        """
        try:
            table = self._client.get_table(name_table)
        except NotFound:
            print(f"Table [{name_table}] does not exist.")
            return

        # Define new SchemaField
        new_field = SchemaField(name=name_col, field_type=type_col, mode="NULLABLE")

        # Append the new field to the existing schema
        updated_schema = list(table.schema) + [new_field]
        table.schema = updated_schema

        # Update table schema
        table = self._client.update_table(table=table, fields=["schema"], retry=Retry())

        if self._verbose:
            print(f"Added column to table [{name_table}]:")
            print(f"  - {type_col}: {name_col}")