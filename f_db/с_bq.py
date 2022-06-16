from tenacity import retry, stop_after_attempt
from google.cloud import bigquery
from f_logging.dec import log_all_methods, log_info_without_self
import pandas as pd
import os

"""
logging.basicConfig(filename='test.log',
                    level=logging.WARNING,
                    filemode='w',
                    encoding='utf-8',
                    format='%(asctime)s: %(levelname)s: %(pathname)s: '
                           '%(funcName)s: %(message)s')
"""


@log_all_methods(decorator=log_info_without_self)
class BigQuery:

    credentials_path = 'd:\\professor\\gcp\\big_query.json'
    # dataset = 'crafty-stock-253813.tiktok'

    def __init__(self, credentials_path: str = None):
        """
        ========================================================================
         Description: Constructor - Initialize the Connection.
        ========================================================================
        """
        if credentials_path:
            self.credentials_path = credentials_path
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials_path
        self._client = bigquery.Client()

    def select(self,
               query: str,  # SQL-Query or Table-Name
               limit: int = -1
               ) -> pd.DataFrame:
        """
        ========================================================================
         Description: Load Query Results into DataFrame.
        ========================================================================
        """
        if ' ' not in query:
            tname = query
            query = f'select * from {tname}'
        if limit > -1:
            query += f' limit {limit}'
        df = self._client.query(query).result().to_dataframe()
        return df

    def run(self, command: str) -> None:
        """
        ========================================================================
         Run BigQuery Command.
        ========================================================================
        """
        job = self._client.query(command)
        job.result()

    def create(self,
               tname: str,
               cols: 'list of str') -> None:
        """
        ========================================================================
         Description: Create Table by given TName and Cols Signature.
        ========================================================================
        """
        self.drop(tname, report=False)
        str_cols = ','.join(cols)
        self.run(f'create table {tname}({str_cols})')

    def ctas(self,
             tname: str,
             query: str) -> None:
        """
        ========================================================================
         Description: Create Table (tname) as Query.
        ========================================================================
        """
        job_config = bigquery.QueryJobConfig(destination=tname)
        self.drop(tname, report=False)
        job = self._client.query(query=query, job_config=job_config)
        job.result()

    def count(self, tname: str) -> int:
        """
        ========================================================================
         Description: Return Number of Rows in the Table.
        ========================================================================
        """
        df = self.select(f'select count(*) from {tname}')
        cnt = int(df.iloc(0)[0][0])
        return cnt

    def is_exists(self, tname: str) -> bool:
        """
        ========================================================================
         Description: Return True if there exists table with the given name.
        ========================================================================
        """
        try:
            self.count(tname)
            return True
        except Exception as e:
            return False

    @retry(stop=stop_after_attempt(100))
    def insert(self,
               tname: str,
               d: dict) -> None:
        """
        ========================================================================
         Description: Insert Row-Values into TName Table.
        ========================================================================
        """
        table = self._client.get_table(tname)
        self._client.insert_rows(table=table, rows=[d])

    def insert_into(self,
                    tname_from: str,
                    tname_to: str,
                    cols: list = None) -> None:
        """
        ========================================================================
         Description: Insert rows from one table into another.
        ========================================================================
        """
        if cols:
            str_cols = ','.join(cols)
            command = f"""insert into {tname_to}({str_cols})
                          select {str_cols} from {tname_from}
                        """
        else:
            command = f'insert into {tname_to} select * from {tname_from}'
        self.run(command)

    def load(self,
             df: pd.DataFrame,
             tname: str,
             append: bool = False) -> None:
        """
        ========================================================================
         Description: Load DataFrame into Sqlite Table.
        ========================================================================
        """
        if_exists = 'append' if append else 'replace'
        self.drop(tname, report=False)
        # self._client.load_table_from_dataframe(df, destination=tname)
        df.to_gbq(destination_table=tname, if_exists=if_exists)

    def drop(self, tname: str, report: bool = False) -> None:
        """
        ========================================================================
         Description: Drop Table (if exists).
        ========================================================================
        """
        command = f'drop table {tname}'
        self.run(command)

    def close(self):
        """
        ========================================================================
         Description: Close the BigQuery connection.
        ========================================================================
        """
        self._client.close()
