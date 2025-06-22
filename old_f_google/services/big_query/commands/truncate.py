from old_f_google.services.big_query.abc.command import Command
from google.api_core.exceptions import NotFound


class Truncate(Command):
    """
    ============================================================================
     BigQuery Truncate-Table.
    ============================================================================
    """

    def table(self,
              name_table: str,
              verbose: bool = None) -> None:
        """
        ========================================================================
         Truncate Table.
        ========================================================================
        """
        if verbose is not None:
            self._verbose = verbose
        try:
            self._client.query(f'truncate table {name_table}')
            if self._verbose:
                print(f'Table [{name_table}] has been truncated')
        except NotFound:
            if self._verbose:
                print(f'Table [{name_table}] does not exist and cannot be truncated')
