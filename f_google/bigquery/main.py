from google.cloud import bigquery
from f_google.auth import Auth, ServiceAccount
import pandas as pd


class BigQuery:
    """
    ============================================================================
     BigQuery Client.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 account: ServiceAccount = ServiceAccount.RAMI) -> None:
        """
        ========================================================================
         Init BigQuery Client with the given Service Account.
        ========================================================================
        """
        creds = Auth.get_creds(account=account)
        self._client = bigquery.Client(credentials=creds,
                                       project=creds.project_id)

    def select(self,
               query: str,
               limit: int = -1) -> pd.DataFrame:
        """
        ========================================================================
         Run a SELECT query and return results as DataFrame.
         If query has no spaces, it is treated as a table name.
        ========================================================================
        """
        if ' ' not in query:
            query = f'select * from {query}'
        if limit > -1:
            query += f' limit {limit}'
        return self._client.query(query).result().to_dataframe()

    def select_list(self,
                    query: str,
                    col: str = None) -> list[str]:
        """
        ========================================================================
         Return a single column as list[str].
         If col is None, return the first column.
        ========================================================================
        """
        df = self.select(query=query)
        if col:
            values = df[col].to_list()
        else:
            values = df.iloc[:, 0].to_list()
        return [str(x) for x in values]

    def select_value(self, query: str) -> any:
        """
        ========================================================================
         Return the first value (first row, first column).
        ========================================================================
        """
        df = self.select(query=query)
        return df.iloc[0][0]

    def run(self, command: str) -> None:
        """
        ========================================================================
         Run a BigQuery command (DDL/DML).
        ========================================================================
        """
        job = self._client.query(command)
        job.result()

    def create(self,
               tname: str,
               cols: list[str]) -> None:
        """
        ========================================================================
         Create a Table with the given columns. Drops if exists.
        ========================================================================
        """
        self.drop(tname=tname)
        str_cols = ','.join(cols)
        self.run(command=f'create table {tname}({str_cols})')

    def insert_rows(self,
                    tname: str,
                    rows: list[dict]) -> None:
        """
        ========================================================================
         Insert rows into a BigQuery Table.
        ========================================================================
        """
        table = self._client.get_table(tname)
        errors = self._client.insert_rows(table=table,
                                          rows=rows,
                                          skip_invalid_rows=True)
        if errors:
            msg = errors[0]['errors'][0]['message']
            raise Exception(f'{msg}\n{rows}')

    def count(self, tname: str) -> int:
        """
        ========================================================================
         Return the number of rows in a Table.
        ========================================================================
        """
        df = self.select(query=f'select count(*) from {tname}')
        return int(df.iloc[0][0])

    def is_exists(self, tname: str) -> bool:
        """
        ========================================================================
         Return True if the Table exists.
        ========================================================================
        """
        try:
            self._client.get_table(tname)
            return True
        except Exception:
            return False

    def drop(self, tname: str) -> None:
        """
        ========================================================================
         Drop a Table (if exists).
        ========================================================================
        """
        command = f'drop table if exists {tname}'
        self.run(command=command)

    def cols(self, tname: str) -> list[str]:
        """
        ========================================================================
         Return column names of a Table.
        ========================================================================
        """
        table = self._client.get_table(tname)
        return [field.name for field in table.schema]

    def close(self) -> None:
        """
        ========================================================================
         Close the BigQuery Client.
        ========================================================================
        """
        self._client.close()
