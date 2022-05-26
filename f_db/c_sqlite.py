import sqlite3
import pandas as pd
from f_utils import u_str
from f_data_structure import u_graph


class SQLite:

    def __init__(self, db_file: str = ':memory:'):
        """
        ========================================================================
         Description: Constructor. Init Connection.
        ========================================================================
        """
        self._db_file = db_file
        self._con = None
        self._cursor = None

    def open(self) -> (bool, str):
        """
        ========================================================================
         Description: Open Connection and Cursor to DataBase.
        ========================================================================
        """
        try:
            self._con = sqlite3.connect(self._db_file)
            self._cursor = self._con.cursor()
        except Exception as e:
            return None, e
        return self, f'DataBase {self._db_file} was successfully connected'

    def run(self, command: str) -> (bool, str):
        """
        ========================================================================
         Return: bool (True if the Command executed successfully).
        ========================================================================
        """
        try:
            self._cursor.execute(command)
            return True, 'SQLite command executed successfully'
        except Exception as e:
            return False, e

    def create(self,
               tname: str,
               cols: list) -> (bool, str):
        """
        ========================================================================
         Description: Create Table by given TName and Cols Signature.
        ========================================================================
        """
        self.drop(tname)
        str_cols = ','.join(cols)
        ans = self.run(f'create table {tname}({str_cols})')
        if ans:
            return True, f'Table {tname} was successfully created'
        return ans

    def select(self,
               query: str,  # SQL-Query or Table-Name
               limit: int = -1
               ) -> (pd.DataFrame, str):
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
        try:
            df = pd.read_sql_query(con=self._con, sql=query)
            return df, f'[{len(df):,} rows] were loaded into the DataFrame'
        except Exception as e:
            return None, e

    def to_list(self,
                query: str,  # SQL-Query or Table-Name
                col: str = None) -> (list, str):
        """
        ========================================================================
         Description: Return Specified Column as a List of str.
                        If a Column-Name is not given - Return First Column.
        ========================================================================
        """
        ans = self.select(query)
        if not ans:
            return ans
        df = ans[0]
        if col:
            try:
                li = df[col].to_list()
            except Exception as e:
                return None, e
        else:
            li = df.iloc[:, 0].to_list()
        li = [str(x) for x in li]
        return li, f'{len(li)} rows were retrieved into the list'

    def select_first(self,
                     query: str  # SQL-Query or Table-Name
                     ) -> (any, str):
        """
        ========================================================================
         Description: Return First Value of the Table (first row and column).
        ========================================================================
        """
        if ' ' not in query:
            tname = query
            query = f'select * from {tname}'
        try:
            self._cursor.execute(query)
            return self.cursor.fetchone()[0], None
        except Exception as e:
            return None, e

    def load(self,
             df: pd.DataFrame,
             tname: str,
             with_index: bool = False,
             ) -> (bool, str):
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
            msg = f"DataFrame loaded into the Table '{tname}' [{len(df):,} rows"
            return True, msg
        except Exception as e:
            return False, e

    def drop(self, tname: str) -> (bool, str):
        """
        ========================================================================
         Description: Drop Table (if exists).
        ========================================================================
        """
        command = f'drop table {tname}'
        ans = self.run(command)
        if not ans[0]:
            return ans
        return True, f'Table {tname} was successfully dropped'

    def ctas(self,
             tname: str,
             query: str) -> (bool, str):
        """
        ========================================================================
         Description: Create Table (tname) as Query.
        ========================================================================
        """
        self.drop(tname)
        query = f'create table {tname} as {query}'
        ans = self.run(query)
        if not ans[0]:
            return ans
        cnt = self.count(tname)[0]
        msg = f"Table '{tname}' successfully created [{cnt} rows]"
        return True, msg

    def count(self, tname: str) -> (int, str):
        """
        ========================================================================
         Description: Return Number of Rows in the Table.
        ========================================================================
        """
        (count, msg) = self.select_first(f'select count(*) from {tname}')
        if count:
            return int(count), msg
        return count, msg

    def is_exists(self, tname: str) -> bool:
        """
        ========================================================================
         Description: Return True if there exists table with the given name.
        ========================================================================
        """
        val, _ = self.select_first(tname)
        return True if val else False

    def insert(self,
               tname: str,
               values: list,
               cols: list = None) -> (bool, str):
        """
        ========================================================================
         Description: Insert Row-Values into TName Table.
        ========================================================================
        """
        values = (u_str.wrap(s, "'") for s in values)
        str_values = ','.join(values)
        str_cols = f'({",".join(cols)})' if cols else ''
        command = f'insert into {tname}{str_cols} values({str_values})'
        ans = self.run(command)
        if ans:
            self.commit()
        return ans

    def insert_into(self,
                    tname_from: str,
                    tname_to: str,
                    cols: list = None) -> (bool, str):
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
        ans = self.run(command)
        if ans:
            self.commit()
        return ans

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
        df, msg = self.select(query=tname, limit=0)
        if df is None:
            return df, f'Cannot retrieve Column-Names: {msg}'
        return df.columns.to_list()

    def commit(self) -> None:
        """
        ========================================================================
         Description: Commit the DataBase.
        ========================================================================
        """
        self._con.commit()

    def close(self, with_commit: bool = True) -> None:
        """
        ========================================================================
         Description: Close Sqlite Cursor and Connection.
        ========================================================================
        """
        if with_commit:
            self.commit()
        self._cursor.close()
        self._con.close()
