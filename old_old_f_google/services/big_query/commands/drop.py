from old_old_f_google.services.big_query.abc.command import Command
from google.api_core.exceptions import NotFound


class Drop(Command):
    """
    ============================================================================
     BigQuery Drop-Commands.
    ============================================================================
    """

    def table(self,
              tname: str,
              verbose: bool = None) -> None:
        """
        ========================================================================
         Drop Table if Exists.
        ========================================================================
        """
        if verbose is not None:
            self._verbose = verbose
        try:
            self._client.delete_table(table=tname)
            if self._verbose:
                print(f'Table [{tname}] has been dropped')
        except NotFound:
            if self._verbose:
                print(f'Table [{tname}] does not exist and cannot be dropped')
