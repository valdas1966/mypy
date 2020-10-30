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
        df = pd.DataFrame()
        try:
            df = pd.read_sql_query(con=self.con, sql=query)
            if verbose:
                print(f'{query}\n{len(df)} rows were loaded into the DataFrame')
        except Exception as e:
            print(f'Error in Selecting Query: {e}\n{query}')
        return df

    def load(self, df, tname, with_index=False, verbose=True):
        assert type(df) == pd.DataFrame()

        df.to_sql(con=self.con, name=tname, if_exists='replace',
                  index=with_index, df=df)
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
        return -1

