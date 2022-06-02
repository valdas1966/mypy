import sqlite3
import pandas as pd
from f_utils import u_str
from f_utils.u_inspect import emsg
from f_data_structure import u_graph


class SQLite:

    def __init__(self, db_file: str = ':memory:'):
        """
        ========================================================================
         Description: Constructor. Init Connection.
        ========================================================================
        """
        try:
            self._db_file = db_file
            self._con = sqlite3.connect(self._db_file)
            self._cursor = self._con.cursor()
        except Exception as e:
            msg = emsg({'db_file': db_file})
            raise Exception(f'{msg}\n{e}')

    def run(self, command: str) -> None:
        """
        ========================================================================
         Run SQLite Command.
        ========================================================================
        """
        try:
            self._cursor.execute(command)
        except Exception as e:
            msg = emsg({'command': command})
            raise Exception(f'{msg}\n{e}')

    def create(self,
               tname: str,
               cols: list[str]) -> None:
        """
        ========================================================================
         Description: Create Table by given TName and Cols Signature.
        ========================================================================
        """
        try:
            self.drop(tname, report=False)
            str_cols = ','.join(cols)
            self.run(f'create table {tname}({str_cols})')
        except Exception as e:
            msg = emsg({'tname': tname, 'cols': cols})
            raise Exception(f'{msg}\n{e}')

    def select(self,
               query: str,  # SQL-Query or Table-Name
               limit: int = -1
               ) -> pd.DataFrame:
        """
        ========================================================================
         Description: Load Query Results into DataFrame.
        ========================================================================
        """
        try:
            if ' ' not in query:
                tname = query
                query = f'select * from {tname}'
            if limit > -1:
                query += f' limit {limit}'
            return pd.read_sql_query(con=self._con, sql=query)
        except Exception as e:
            msg = emsg({'query': query, 'limit': limit})
            raise Exception(f'{msg}\n{e}')

    def to_list(self,
                query: str,  # SQL-Query or Table-Name
                col: str = None) -> list:
        """
        ========================================================================
         Description: Return Specified Column as a List of str.
                        If a Column-Name is not given - Return First Column.
        ========================================================================
        """
        try:
            df = self.select(query)
            if col:
                li = df[col].to_list()
            else:
                li = df.iloc[:, 0].to_list()
            return [str(x) for x in li]
        except Exception as e:
            msg = emsg({'query': query, 'col': col})
            raise Exception(f'{msg}\n{e}')

    def select_first(self,
                     query: str  # SQL-Query or Table-Name
                     ) -> any:
        """
        ========================================================================
         Description: Return First Value of the Table (first row and column).
        ========================================================================
        """
        try:
            if ' ' not in query:
                tname = query
                query = f'select * from {tname} limit 1'
            self._cursor.execute(query)
            return self.cursor.fetchone()[0]
        except Exception as e:
            msg = emsg({'query': query})
            raise Exception(f'{msg}\n{e}')

    def load(self,
             df: pd.DataFrame,
             tname: str,
             with_index: bool = False) -> None:
        """
        ========================================================================
         Description: Load DataFrame into Sqlite Table.
        ========================================================================
        """
        try:
            if with_index:
                df.index.names = ['i']
            df.to_sql(con=self._con, name=tname, if_exists='replace',
                      index=with_index)
        except Exception as e:
            msg = emsg({'df': df, 'tname': tname, 'with_index': with_index})
            raise Exception(f'{msg}\n{e}')

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
                raise Exception(f'{msg}\n{e}')

    def ctas(self,
             tname: str,
             query: str) -> None:
        """
        ========================================================================
         Description: Create Table (tname) as Query.
        ========================================================================
        """
        command = None
        try:
            self.drop(tname, report=False)
            command = f'create table {tname} as {query}'
            self.run(command)
        except Exception as e:
            msg = emsg({'tname': tname, 'query': query, 'command': command})
            raise Exception(f'{msg}\n{e}')

    def count(self, tname: str) -> int:
        """
        ========================================================================
         Description: Return Number of Rows in the Table.
        ========================================================================
        """
        try:
            return int(self.select_first(f'select count(*) from {tname}'))
        except Exception as e:
            msg = emsg({'tname': tname})
            raise Exception(f'{msg}\n{e}')

    def is_exists(self, tname: str) -> bool:
        """
        ========================================================================
         Description: Return True if there exists table with the given name.
        ========================================================================
        """
        try:
            self.select_first(tname)
            return True
        except Exception as e:
            return False

    def insert(self,
               tname: str,
               values: list,
               cols: list = None) -> None:
        """
        ========================================================================
         Description: Insert Row-Values into TName Table.
        ========================================================================
        """
        try:
            values = (u_str.wrap(s, "'") for s in values)
            str_values = ','.join(values)
            str_cols = f'({",".join(cols)})' if cols else ''
            command = f'insert into {tname}{str_cols} values({str_values})'
            self.run(command)
        except Exception as e:
            msg = emsg({'tname': tname, 'values': values, 'cols': cols})
            raise Exception(f'{msg}\n{e}')

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
            self.commit()
        except Exception as e:
            msg = emsg({'tname_from': tname_from, 'tname_to': tname_to,
                        'cols': cols})
            raise Exception(f'{msg}\n{e}')

    def get_descendants(self,
                        tname: str,
                        col_parent: str,
                        col_child: str) -> any:
        query = f"""
                    select
                        {col_parent},
                        {col_child}
                    from
                        {tname}
                    where
                        id_parent = {col_parent}"""

    def cols(self, tname: str) -> list:  # list of str
        """
        ========================================================================
         Description: Return Column-Names of the given Table-Name.
        ========================================================================
        """
        try:
            df = self.select(query=tname, limit=0)
            return df.columns.to_list()
        except Exception as e:
            msg = emsg({'tname': tname})
            raise Exception(f'{msg}\n{e}')

    def commit(self) -> None:
        """
        ========================================================================
         Description: Commit the DataBase.
        ========================================================================
        """
        try:
            self._con.commit()
        except Exception as e:
            msg = emsg(dict())
            raise Exception(f'{msg}\n{e}')

    def close(self, with_commit: bool = True) -> None:
        """
        ========================================================================
         Description: Close Sqlite Cursor and Connection.
        ========================================================================
        """
        try:
            if with_commit:
                self.commit()
            self._cursor.close()
            self._con.close()
        except Exception as e:
            msg = emsg()
            raise Exception(f'{msg}\n{e}')
