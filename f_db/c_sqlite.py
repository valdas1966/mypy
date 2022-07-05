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
        self._con = sqlite3.connect(self._db_file)
        self._cursor = self._con.cursor()

    def run(self, command: str) -> None:
        """
        ========================================================================
         Run SQLite Command.
        ========================================================================
        """
        self._cursor.execute(command)

    def create(self,
               tname: str,
               cols: 'list[str]') -> None:
        """
        ========================================================================
         Description: Create Table by given TName and Cols Signature.
        ========================================================================
        """
        self.drop(tname, report=False)
        str_cols = ','.join(cols)
        self.run(f'create table {tname}({str_cols})')

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
        return pd.read_sql_query(con=self._con, sql=query)

    def to_list(self,
                query: str,  # SQL-Query or Table-Name
                col: str = None) -> list:
        """
        ========================================================================
         Description: Return Specified Column as a List of str.
                        If a Column-Name is not given - Return First Column.
        ========================================================================
        """
        df = self.select(query)
        if col:
            li = df[col].to_list()
        else:
            li = df.iloc[:, 0].to_list()
        return [str(x) for x in li]

    def select_first(self,
                     query: str  # SQL-Query or Table-Name
                     ) -> any:
        """
        ========================================================================
         Description: Return First Value of the Table (first row and column).
        ========================================================================
        """
        if ' ' not in query:
            tname = query
            query = f'select * from {tname} limit 1'
        self._cursor.execute(query)
        return self.cursor.fetchone()[0]

    def load(self,
             df: pd.DataFrame,
             tname: str,
             with_index: bool = False) -> None:
        """
        ========================================================================
         Description: Load DataFrame into Sqlite Table.
        ========================================================================
        """
        if with_index:
            df.index.names = ['i']
        df.to_sql(con=self._con, name=tname, if_exists='replace',
                  index=with_index)

    def drop(self, tname: str, report: bool = False) -> None:
        """
        ========================================================================
         Description: Drop Table (if exists).
        ========================================================================
        """
        command = f'drop table {tname}'
        self.run(command)

    def ctas(self,
             tname: str,
             query: str) -> None:
        """
        ========================================================================
         Description: Create Table (tname) as Query.
        ========================================================================
        """
        self.drop(tname, report=False)
        command = f'create table {tname} as {query}'
        self.run(command)

    def count(self, tname: str) -> int:
        """
        ========================================================================
         Description: Return Number of Rows in the Table.
        ========================================================================
        """
        return int(self.select_first(f'select count(*) from {tname}'))

    def is_exists(self, tname: str) -> bool:
        """
        ========================================================================
         Description: Return True if there exists table with the given name.
        ========================================================================
        """
        try:
            self.select_first(tname)
            return True
        except Exception:
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
        values = (u_str.wrap(s, "'") for s in values)
        str_values = ','.join(values)
        str_cols = f'({",".join(cols)})' if cols else ''
        command = f'insert into {tname}{str_cols} values({str_values})'
        self.run(command)

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
        self.commit()

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
        df = self.select(query=tname, limit=0)
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
