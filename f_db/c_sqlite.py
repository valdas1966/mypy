import sqlite3
import pandas as pd
from f_utils import u_str
from f_data_structure import u_graph



class SQLite:

    def __init__(self, db_file=':memory:'):
        """
        ========================================================================
         Description: Constructor. Init Connection.
        ========================================================================
        """
        self.con = sqlite3.connect(db_file)
        self.cursor = self.con.cursor()

    def create(self, tname, cols, verbose=False):
        """
        ========================================================================
         Description: Create Table by given TName and Cols Signature.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. tname: str
            2. cols : list of str
            3. verbose : bool
        ========================================================================
        """
        self.drop(tname)
        str_cols = ','.join(cols)
        self.run(f'create table {tname}({str_cols})', verbose)

    def select(self, query, verbose=True):
        """
        ========================================================================
         Description: Load Query Results into DataFrame.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. query : str (SQL Query or Table Name).
        ========================================================================
         Return: DataFrame
        ========================================================================
        """
        assert type(query) == str
        if ' ' not in query:
            query = f'select * from {query}'
        try:
            df = pd.read_sql_query(con=self.con, sql=query)
            if verbose:
                print(f'[{len(df):,} rows] were loaded into the DataFrame')
            return df
        except Exception as e:
            print(f'Error in Selecting Query: {e}\n{query}')

    def to_list(self, query, col=None):
        """
        ========================================================================
         Description: Return Specified DF-Column as a List.
                        If a Column-Name is not given - Return First Column.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. query : str (can take only table-name).
            2. col : str
        ========================================================================
         Return: list
        """
        df = self.select(query, verbose=False)
        li = None
        if col:
            li = df[col].to_list()
        else:
            li = df.iloc[:, 0].to_list()
        return [str(x) for x in li]

    def select_value(self, query):
        """
        ========================================================================
         Description: Return First Value of the Table (first row and column).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. query : str (SQLite Query).
        ========================================================================
         Return: obj
        ========================================================================
        """
        df = self.select(query, verbose=False)
        return df.loc[0][0]

    def load(self, df, tname, with_index=False, verbose=True):
        """
        ========================================================================
         Description: Load DataFrame into Sqlite Table.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. df : DataFrame
            2. tname : str
            3. with_index : bool
            4. verbose : bool
        ========================================================================
        """
        assert type(df) == pd.DataFrame
        assert type(tname) == str
        assert type(with_index) == bool
        assert type(verbose) == bool
        try:
            if with_index:
                df.index.names = ['i']
            df.to_sql(con=self.con, name=tname, if_exists='replace',
                      index=with_index)
            if verbose:
                print(f"DataFrame loaded into the Table '{tname}' [{len(df):,} "
                      f"rows]")
        except Exception as e:
            print(f'Error in Loading DF into Table {tname}: {e}')

    def run(self, command, verbose=True):
        """
        ========================================================================
         Description: Run SQLite Command.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. command : str
            2. verbose : bool
        ========================================================================
         Return: bool (True if the Command executed successfully).
        ========================================================================
        """
        try:
            self.cursor.execute(command)
            if verbose:
                print('SQLite command executed successfully')
            return True
        except Exception as e:
            if verbose:
                print(f'Error in: {command}\n{e}')
            return False

    def drop(self, tname):
        """
        ========================================================================
         Description: Drop Table (if exists).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. tname : str (Table Name to Drop).
        ========================================================================
         Return: bool
        ========================================================================
        """
        command = f'drop table {tname}'
        return self.run(command=command, verbose=False)

    def ctas(self, tname, query, verbose=True):
        """
        ========================================================================
         Description: Create Table (tname) as Query.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. tname : str
            2. query : str
            3. verbose : bool
        ========================================================================
        """
        try:
            self.cursor.execute(f'drop table {tname}')
        except Exception as e:
            pass
        query = f'create table {tname} as {query}'
        try:
            self.cursor.execute(query)
            cnt = f'{self.count(tname):,}'
            if verbose:
                print(f"Table '{tname}' successfully created [{cnt} rows]")
        except Exception as e:
            print(f'Error in Creating Table {tname}: {e}\n{query}')

    def count(self, tname, verbose=True):
        """
        ========================================================================
         Description: Return Number of Rows in the Table.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. tname : str (Table Name).
            2. verbose : bool
        ========================================================================
         Return: int (Number of Rows in the Table, -1 on Error).
        ========================================================================
        """
        assert type(tname) == str
        try:
            self.cursor.execute(f'select count(*) from {tname}')
            return self.cursor.fetchone()[0]
        except Exception as e:
            if verbose:
                print(f'Error in Counting Table: {e}\n{tname}')
            return None

    def is_exists(self, tname):
        """
        ========================================================================
         Description: Return True if there exists table with the given name.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. tname : str
        ========================================================================
         Return: bool
        ========================================================================
        """
        cnt = self.count(tname, verbose=False)
        if cnt is None:
            return False
        return True

    def insert(self, tname, values, cols=None, verbose=False):
        """
        ========================================================================
         Description: Insert Row-Values into TName Table.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. tname : str
            2. values : list
            3. cols : list of str
            4. verbose : bool
        ========================================================================
        """
        values = (u_str.wrap(s, "'") for s in values)
        str_values = ','.join(values)
        str_cols = f'({",".join(cols)})' if cols else ''
        command = f'insert into {tname}{str_cols} values({str_values})'
        self.run(command, verbose)
        self.commit()

    def insert_into(self, tname_from, tname_to, cols=None, verbose=False):
        """
        ========================================================================
         Description: Insert rows from one table into another.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. tname_from : str (Table Name from where to insert).
            2. tname_to : str (Table Name to insert into).
            3. cols : list of str (Columns Names to Insert).
            4. verbose : bool
        ========================================================================
        """
        if cols:
            str_cols = ','.join(cols)
            command = f"""insert into {tname_to}({str_cols})
                          select {str_cols} from {tname_from}
                        """
        else:
            command = f'insert into {tname_to} select * from {tname_from}'
        self.run(command, verbose)
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



    def cols(self, tname):
        """
        ========================================================================
         Description: Return Column-Names of the given Table.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. tname : str
        ========================================================================
         Return: list of str
        ========================================================================
        """
        query = f'select * from {tname} limit 0'
        return self.select(query).columns.to_list()

    def commit(self):
        self.con.commit()

    def close(self):
        """
        ========================================================================
         Description: Close Sqlite Cursor and Connection.
        ========================================================================
        """
        self.cursor.close()
        self.con.close()
