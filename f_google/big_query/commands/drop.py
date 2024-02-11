from f_google.big_query.abc.command import Command


class Drop(Command):
    """
    ============================================================================
     BigQuery Drop-Commands.
    ============================================================================
    """

    def table(self, name: str) -> None:
        """
        ========================================================================
         Drop Table if Exists.
        ========================================================================
        """
        if self._verbose:
            table = self._client.get_table(table=name)
        self._client.delete_table(table=name,
                                  not_found_ok=True)
        if self._verbose:
            print(f'Table [{name}] has been dropped.')
