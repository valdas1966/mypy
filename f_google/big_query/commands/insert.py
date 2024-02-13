from f_google.big_query.abc.command import Command
from f_google.strategies.retry import Retry
from f_utils import u_datetime


class Insert(Command):
    """
    ============================================================================
     BigQuery Insert-Commands.
    ============================================================================
    """

    def rows(self,
             tname: str,
             rows: list[dict]) -> list[dict]:
        """
        ========================================================================
         Insert Rows into BigQuery Table and return List of Errors.
        ========================================================================
        """
        table = self._client.get_table(tname)
        errors = self._client.insert_rows_json(table=table,
                                               json_rows=rows,
                                               retry=Retry())
        if self._verbose:
            if not errors:
                print(f'[{len(rows)}] rows were inserted into [{tname}].')
            else:
                print(f'There were errors inserting rows into [{tname}].')
                print(errors)
        return errors

    def rows_inserted(self,
                      tname: str,
                      rows: list[dict]) -> list[dict]:
        """
        ========================================================================
         Add to Rows the current DateTime and Insert them into the Table.
        ========================================================================
        """
        sysdate = u_datetime.now(format='LOG', is_utc=True)
        for row in rows:
            row['inserted'] = sysdate
        return self.rows(tname=tname, rows=rows)
