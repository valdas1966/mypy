from old_old_f_google.services.big_query.abc.command import Command
from old_old_f_google.strategies.retry import Retry
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
    
    def select(self,
               name_table: str,
               query: str) -> list[dict]:
        """
        ========================================================================
         1. Execute 'INSERT INTO name_table SELECT ...'
             using the provided query body.
         Return a list of errors (empty if successful).
        ========================================================================
        """
        query_full = f'INSERT INTO {name_table} {query}'
        job = self._client.query(query=query_full, retry=Retry())
        # Wait for completion
        job.result()  
        
        # Number of rows inserted
        rows = job.num_dml_affected_rows or 0

        # List of errors (empty if successful)
        errors = job.errors or []

        if self._verbose:
            if not errors:
                print(f'Query executed successfully! [{rows}] rows inserted')
                print()
                print(query_full)
            else:
                print(f'Errors occurred while executing query:\n{query_full}')
                print(errors)

        return errors
