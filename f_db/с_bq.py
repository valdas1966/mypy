from f_utils.u_inspect import emsg
from google.cloud import bigquery
import pandas as pd
import logging
import os


logging.basicConfig(filename='test.log',
                    level=logging.WARNING,
                    filemode='w',
                    encoding='utf-8',
                    format='%(asctime)s: %(levelname)s: %(pathname)s: '
                           '%(funcName)s: %(message)s')


class BigQuery:

    credentials_path = 'd:\\professor\\gcp\\big_query.json'
    dataset = 'crafty-stock-253813.tiktok'

    def __init__(self, credentials_path: str = None):
        """
        ========================================================================
         Description: Constructor - Initialize the Connection.
        ========================================================================
        """
        logging.info('BEGIN FUNC')
        logging.info(f'credentials_path={credentials_path}, '
                     f'{type(credentials_path)}')
        if credentials_path:
            self.credentials_path = credentials_path
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials_path
        try:
            self._client = bigquery.Client()
            logging.info('BigQuery connection was successfully established')
        except Exception as e:
            logging.info(f'EXCEPTION: {e}')
            msg = emsg({'credentials_path': self.credentials_path})
            raise Exception(f'{msg}\n{e.args[0]}')
        finally:
            logging.info('END FUNC')

    def select(self,
               query: str,  # SQL-Query or Table-Name
               limit: int = -1
               ) -> pd.DataFrame:
        """
        ========================================================================
         Description: Load Query Results into DataFrame.
        ========================================================================
        """
        logging.info('BEGIN FUNC')
        logging.info(f'query={query}, {type(query)}')
        logging.info(f'limit={limit}, {type(limit)}')
        try:
            if ' ' not in query:
                tname = query
                query = f'select * from {tname}'
            if limit > -1:
                query += f' limit {limit}'
            logging.info(f'query={query}, {type(query)}')
            df = self._client.query(query).result().to_dataframe()
            logging.info(f'Query was successfully loaded into the DataFrame '
                         f'[{len(df)} rows]')
            return df
        except Exception as e:
            logging.info(f'EXCEPTION: {e}')
            msg = emsg({'query': query, 'limit': limit})
            raise Exception(f'{msg}\n{e.args[0]}')
        finally:
            logging.info('END FUNC')

    def run(self, command: str) -> None:
        """
        ========================================================================
         Run BigQuery Command.
        ========================================================================
        """
        logging.info('BEGIN FUNC')
        logging.info(f'command={command}, {type(command)}')
        try:
            job = self._client.query(command)
            job.result()
            logging.info('BigQuery command was successfully executed')
        except Exception as e:
            logging.info(f'EXCEPTION: {e}')
            msg = emsg({'command': command})
            raise Exception(f'{msg}\n{e}')
        finally:
            logging.info('END FUNC')

    def create(self,
               tname: str,
               cols: 'list of str') -> None:
        """
        ========================================================================
         Description: Create Table by given TName and Cols Signature.
        ========================================================================
        """
        logging.info('BEGIN FUNC')
        logging.info(f'tname={tname}, {type(tname)}')
        logging.info(f'cols={cols}, {type(cols)}')
        try:
            self.drop(tname, report=False)
            str_cols = ','.join(cols)
            self.run(f'create table {tname}({str_cols})')
            logging.info('BigQuery table was successfully created')
        except Exception as e:
            logging.info(f'EXCEPTION: {e}')
            msg = emsg({'tname': tname, 'cols': cols})
            raise Exception(f'{msg}\n{e}')
        finally:
            logging.info('END FUNC')

    def ctas(self,
             tname: str,
             query: str) -> None:
        """
        ========================================================================
         Description: Create Table (tname) as Query.
        ========================================================================
        """
        logging.info('BEGIN FUNC')
        logging.info(f'tname={tname}, {type(tname)}')
        logging.info(f'query={query}, {type(query)}')
        job_config = bigquery.QueryJobConfig(destination=tname)
        self.drop(tname, report=False)
        try:
            job = self._client.query(query=query, job_config=job_config)
            job.result()
            logging.info(f'BigQuery table was successfully created with '
                         f'{self.count(tname)} rows')
        except Exception as e:
            logging.info(f'EXCEPTION: {e}')
            msg = emsg({'tname': tname, 'query': query})
            raise Exception(f'{msg}\n{e.args[0]}')
        finally:
            logging.info('END FUNC')

    def count(self, tname: str) -> int:
        """
        ========================================================================
         Description: Return Number of Rows in the Table.
        ========================================================================
        """
        logging.info('BEGIN FUNC')
        logging.info(f'tname={tname}, {type(tname)}')
        try:
            df = self.select(f'select count(*) from {tname}')
            cnt = int(df.iloc(0)[0][0])
            logging.info(f'RETURN: {cnt}')
            return cnt
        except Exception as e:
            logging.info(f'EXCEPTION: {e}')
            msg = emsg({'tname': tname})
            raise Exception(f'{msg}\n{e}')
        finally:
            logging.info('END FUNC')

    def is_exists(self, tname: str) -> bool:
        """
        ========================================================================
         Description: Return True if there exists table with the given name.
        ========================================================================
        """
        logging.info('BEGIN FUNC')
        logging.info(f'tname={tname}, {type(tname)}')
        try:
            self.count(tname)
            logging.info('RETURN: True')
            return True
        except Exception as e:
            logging.info('RETURN: False')
            return False
        finally:
            logging.info('END FUNC')

    def insert(self,
               tname: str,
               d: dict) -> None:
        """
        ========================================================================
         Description: Insert Row-Values into TName Table.
        ========================================================================
        """
        logging.info('BEGIN FUNC')
        logging.info(f'tname={tname}, {type(tname)}')
        logging.info(f'd={d}, {type(d)}')
        try:
            table = self._client.get_table(tname)
            self._client.insert_rows(table=table, rows=[d])
            logging.info('Row was successfully inserted into the table')
        except Exception as e:
            logging.info(f'EXCEPTION: {e}')
            msg = emsg({'tname': tname, 'd': d})
            raise Exception(f'{msg}\n{e}')
        finally:
            logging.info('END FUNCTION')

    def insert_into(self,
                    tname_from: str,
                    tname_to: str,
                    cols: list = None) -> None:
        """
        ========================================================================
         Description: Insert rows from one table into another.
        ========================================================================
        """
        try:
            if cols:
                str_cols = ','.join(cols)
                command = f"""insert into {tname_to}({str_cols})
                              select {str_cols} from {tname_from}
                            """
            else:
                command = f'insert into {tname_to} select * from {tname_from}'
            self.run(command)
        except Exception as e:
            msg = emsg({'tname_from': tname_from, 'tname_to': tname_to,
                        'cols': cols})
            raise Exception(f'{msg}\n{e}')

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
        try:
            self.drop(tname, report=False)
            # self._client.load_table_from_dataframe(df, destination=tname)
            df.to_gbq(destination_table=tname, if_exists=if_exists)
        except Exception as e:
            msg = emsg({'df': df, 'tname': tname})
            raise Exception(f'{msg}\n{e.args[0]}')

    def drop(self, tname: str, report: bool = False) -> None:
        """
        ========================================================================
         Description: Drop Table (if exists).
        ========================================================================
        """
        try:
            command = f'drop table {tname}'
            self.run(command)
        except Exception as e:
            if report:
                msg = emsg({'tname': tname, 'report': report})
                raise Exception(f'{msg}\n{e.args[0]}')

    def close(self):
        try:
            self._client.close()
        except Exception as e:
            raise Exception(f'{emsg()}\n{e.args[0]}')


bq = BigQuery()