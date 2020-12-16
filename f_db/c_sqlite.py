import sqlite3
import pandas as pd


class Sqlite:

    def __init__(self):
        """
        ========================================================================
         Description: Constructor. Init Connection.
        ========================================================================
        """
        self.con = sqlite3.connect(':memory:')
        self.cursor = self.con.cursor()

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
            df.to_sql(con=self.con, name=tname, if_exists='replace',
                      index=with_index)
            if verbose:
                print(f"DataFrame loaded into the Table '{tname}' [{len(df):,} "
                      f"rows]")
        except Exception as e:
            print(f'Error in Loading DF into Table {tname}: {e}')

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

    def count(self, tname):
        """
        ========================================================================
         Description: Return Number of Rows in the Table.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. tname : str (Table Name).
        ========================================================================
         Return: int (Number of Rows in the Table, -1 on Error).
        ========================================================================
        """
        assert type(tname) == str
        try:
            self.cursor.execute(f'select count(*) from {tname}')
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(f'Error in Counting Table: {e}\n{tname}')

    def close(self):
        """
        ========================================================================
         Description: Close Sqlite Cursor and Connection.
        ========================================================================
        """
        self.cursor.close()
        self.con.close()
