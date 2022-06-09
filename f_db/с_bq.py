from tenacity import retry, stop_after_attempt
from google.cloud import bigquery
import pandas as pd
import logging
import os

"""
logging.basicConfig(filename='test.log',
                    level=logging.WARNING,
                    filemode='w',
                    encoding='utf-8',
                    format='%(asctime)s: %(levelname)s: %(pathname)s: '
                           '%(funcName)s: %(message)s')
"""


class BigQuery:

    credentials_path = 'd:\\professor\\gcp\\big_query.json'
    # dataset = 'crafty-stock-253813.tiktok'

    def __init__(self, credentials_path: str = None):
        """
        ========================================================================
         Description: Constructor - Initialize the Connection.
        ========================================================================
        """
        logging.info('BEGIN')
        logging.info(f'credentials_path={credentials_path}, '
                     f'{type(credentials_path)}')
        if credentials_path:
            self.credentials_path = credentials_path
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials_path
        self._client = bigquery.Client()
        logging.info('END')

    def select(self,
               query: str,  # SQL-Query or Table-Name
               limit: int = -1
               ) -> pd.DataFrame:
        """
        ========================================================================
         Description: Load Query Results into DataFrame.
        ========================================================================
        """
        logging.info('BEGIN')
        logging.info(f'query={query}, {type(query)}')
        logging.info(f'limit={limit}, {type(limit)}')
        if ' ' not in query:
            tname = query
            query = f'select * from {tname}'
        if limit > -1:
            query += f' limit {limit}'
        logging.info(f'query={query}, {type(query)}')
        df = self._client.query(query).result().to_dataframe()
        logging.info('END')
        return df

    def run(self, command: str) -> None:
        """
        ========================================================================
         Run BigQuery Command.
        ========================================================================
        """
        logging.info('BEGIN')
        logging.info(f'command={command}, {type(command)}')
        job = self._client.query(command)
        job.result()
        logging.info('END')

    def create(self,
               tname: str,
               cols: 'list of str') -> None:
        """
        ========================================================================
         Description: Create Table by given TName and Cols Signature.
        ========================================================================
        """
        logging.info('BEGIN')
        logging.info(f'tname={tname}, {type(tname)}')
        logging.info(f'cols={cols}, {type(cols)}')
        self.drop(tname, report=False)
        str_cols = ','.join(cols)
        self.run(f'create table {tname}({str_cols})')
        logging.info('END')

    def ctas(self,
             tname: str,
             query: str) -> None:
        """
        ========================================================================
         Description: Create Table (tname) as Query.
        ========================================================================
        """
        logging.info('BEGIN')
        logging.info(f'tname={tname}, {type(tname)}')
        logging.info(f'query={query}, {type(query)}')
        job_config = bigquery.QueryJobConfig(destination=tname)
        self.drop(tname, report=False)
        job = self._client.query(query=query, job_config=job_config)
        job.result()
        logging.info('END')

    def count(self, tname: str) -> int:
        """
        ========================================================================
         Description: Return Number of Rows in the Table.
        ========================================================================
        """
        logging.info('BEGIN')
        logging.info(f'tname={tname}, {type(tname)}')
        df = self.select(f'select count(*) from {tname}')
        cnt = int(df.iloc(0)[0][0])
        logging.info('END')
        return cnt

    def is_exists(self, tname: str) -> bool:
        """
        ========================================================================
         Description: Return True if there exists table with the given name.
        ========================================================================
        """
        logging.info('BEGIN')
        logging.info(f'tname={tname}, {type(tname)}')
        try:
            self.count(tname)
            return True
        except Exception as e:
            return False
        finally:
            logging.info('END')

    @retry(stop=stop_after_attempt(100))
    def insert(self,
               tname: str,
               d: dict) -> None:
        """
        ========================================================================
         Description: Insert Row-Values into TName Table.
        ========================================================================
        """
        logging.info('BEGIN')
        logging.info(f'tname={tname}, {type(tname)}')
        logging.info(f'd={d}, {type(d)}')
        table = self._client.get_table(tname)
        logging.info(f'table={table}, {type(table)}')
        self._client.insert_rows(table=table, rows=[d])
        logging.info('END')

    def insert_into(self,
                    tname_from: str,
                    tname_to: str,
                    cols: list = None) -> None:
        """
        ========================================================================
         Description: Insert rows from one table into another.
        ========================================================================
        """
        logging.info('BEGIN')
        logging.info(f'tname_from={tname_from}, {type(tname_from)}')
        logging.info(f'tname_to={tname_to}, {type(tname_to)}')
        if cols:
            str_cols = ','.join(cols)
            command = f"""insert into {tname_to}({str_cols})
                          select {str_cols} from {tname_from}
                        """
        else:
            command = f'insert into {tname_to} select * from {tname_from}'
        self.run(command)
        logging.info('END')

    def load(self,
             df: pd.DataFrame,
             tname: str,
             append: bool = False) -> None:
        """
        ========================================================================
         Description: Load DataFrame into Sqlite Table.
        ========================================================================
        """
        logging.info('BEGIN')
        logging.info(f'df.shape={df.shape if type(df)==pd.DataFrame else None},'
                     f' {type(df)}')
        logging.info(f'tname={tname}, {type(tname)}')
        logging.info(f'append={append}, {type(append)}')
        if_exists = 'append' if append else 'replace'
        self.drop(tname, report=False)
        # self._client.load_table_from_dataframe(df, destination=tname)
        df.to_gbq(destination_table=tname, if_exists=if_exists)
        logging.info('END')

    def drop(self, tname: str, report: bool = False) -> None:
        """
        ========================================================================
         Description: Drop Table (if exists).
        ========================================================================
        """
        logging.info('BEGIN')
        logging.info(f'tname={tname}, {type(tname)}')
        logging.info(f'report={report}, {type(report)}')
        command = f'drop table {tname}'
        self.run(command)
        logging.info('END')

    def close(self):
        """
        ========================================================================
         Description: Close the BigQuery connection.
        ========================================================================
        """
        logging.info('BEGIN')
        self._client.close()
        logging.info('END')
